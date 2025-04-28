import sqlite3
from sqlite3 import Connection


class DatabaseConnection:
    _instance = None

    def __init__(self, db_path: str = "resources/database/perfilador.db"):
        """Inicializa a conexão com o banco de dados"""
        self.db_path = db_path
        self.connection: Connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

    @classmethod
    def get_instance(cls):
        """Cria singleton"""
        if cls._instance is None:
            cls._instance = DatabaseConnection()
        return cls._instance

    def get_connection(self) -> Connection:
        return self.connection

    def close(self):
        if self.connection is not None:
            self.connection.close()
            DatabaseConnection._instance = None
