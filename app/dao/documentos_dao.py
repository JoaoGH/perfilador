import json

from app.dao.base_dao import BaseDAO
from app.model.document import Document


class DocumentoDao(BaseDAO[Document]):

    def __init__(self):
        super().__init__(Document)

    def _get_conversion_map(self) -> dict:
        return {
            "tokens": lambda v: json.loads(v) if v else [],
            'pipeline_executed': lambda v: bool(int(v)) if str(v).isdigit() else bool(v),
            'information_extracted': lambda v: bool(int(v)) if str(v).isdigit() else bool(v)
        }

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
