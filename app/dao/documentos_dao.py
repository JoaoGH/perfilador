import json
from datetime import datetime
from typing import Optional

from app.dao.base_dao import BaseDAO
from app.model.document import Document


class DocumentoDao(BaseDAO[Document]):

    def __init__(self):
        super().__init__(Document)

    def _get_conversion_map(self) -> dict:
        return {
            "tokens": lambda v: json.loads(v) if v else [],
            "pages": lambda v: json.loads(v) if v else [],
            'pipeline_executed': lambda v: bool(int(v)) if str(v).isdigit() else bool(v),
            'information_extracted': lambda v: bool(int(v)) if str(v).isdigit() else bool(v),
            'download_timestamp': self._convert_to_datetime
        }

    def _convert_to_datetime(self, value: str) -> Optional[datetime]:
        """Converte string ISO para datetime"""
        if not value:
            return None
        return datetime.fromisoformat(value) if isinstance(value, str) else value

    def exists_by_hash(self, document_hash: str) -> bool:
        """Verifica se já existe um documento com o hash especificado cadastrado

        Returns:
            bool: True se o documento existe, False caso contrário
        """
        query = f"SELECT COUNT(1) FROM {self.table_name} WHERE hash = ?"
        cursor = self.conn.cursor()

        try:
            cursor.execute(query, (document_hash,))
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"Erro ao verificar existência do documento: {str(e)}")

        return True
