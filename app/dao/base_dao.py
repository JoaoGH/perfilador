import sqlite3
from abc import ABC
from typing import Dict, Optional, List

from app.database.database_connection import DatabaseConnection

class BaseDAO(ABC):
    def __init__(self, table_name: str = None):
        self.conn = DatabaseConnection().get_instance().get_connection()
        self.table_name = table_name

    def insert(self, data: Dict) -> int:
        """Cria novo registro no banco"""

        fields = ", ".join(data.keys())
        placeholders = ", ".join(['?'] * len(data.keys()))

        query = f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})"
        cursor = self.conn.cursor()

        try:
            cursor.execute(query, tuple(data.values()))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Erro ao salvar registro no banco: " + str(e))

    def get(self, id: int) -> Optional[sqlite3.Row]:
        """Buscar regitro pelo ID"""
        query = f"SELECT * FROM {self.table_name} WHERE id = {id}"
        cursor = self.conn.cursor()
        row = cursor.fetchone()
        return row

    def list(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Listar registros no banco"""
        query = f"SELECT * FROM {self.table_name} ORDER BY id LIMIT ? OFFSET ?"
        cursor = self.conn.execute(query, (limit, offset))
        return cursor.fetchall()

    def update(self, id: int, data: Dict) -> bool:
        """Atualizar registro no banco"""

        if not data:
            return False

        fields = ", ".join([f"{k} = ? " for k in data.keys()])
        query = f"UPDATE {self.table_name} SET {fields} WHERE id = {id}"

        values = list(data.values())
        values.append(id)

        cursor = self.conn.cursor()
        cursor.execute(query, tuple(values))
        self.conn.commit()

        return cursor.rowcount > 0

    def remove(self, id: int) -> bool:
        """Remove registro no banco"""

        query = f"DELETE FROM {self.table_name} WHERE id = {id}"
        cursor = self.conn.execute(query, (id,))
        self.conn.commit()

        return cursor.rowcount > 0
