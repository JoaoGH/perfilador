import re
import unicodedata
from typing import List

import nltk

from app.dao.documentos_dao import DocumentoDao
from app.model.document import Document
from app.document_manager import DocumentManager


class PreProcessor:

    def __init__(self):
        # Garante que os recursos do NLTK estão disponíveis
        nltk.download('punkt', quiet=True)
        self.document_manager = DocumentManager()

    def clear(self, text: str) -> str:
        """Executa todas as operações de limpeza básica do texto"""

        if not text:
            return ""

        text = text.strip().lower()
        text = re.sub(r"-[\r\n\t]+", "", text)
        text = re.sub(r"[\r\n\t]+", " ", text)

        for it in ("\.\.", "__", ": ", ":_", ":\."):
            regex = r"(?<=[a-z])(" + it + ")(?=[a-z])"
            text = re.sub(regex, " ", text)

        text = re.sub(r"(?<!\s)\(", " (", text)
        text = re.sub(r"\)(?!\s)", ") ", text)

        text = re.sub(r"_", " ", text)

        text = re.sub(r"\s+", " ", text)

        text = text.replace("|quebra pagina|", self.document_manager.PAGE_SEPARATOR)

        return text

    def normalize(self, text: str) -> str:
        """Executa a normalização do texto"""

        if not text:
            return ""

        # Tabela de tradução
        translation_table = str.maketrans(
            'áàâãäéèêëíìîïóòôõöúùûüçñ',
            'aaaaaeeeeiiiiooooouuuucn'
        )

        text = unicodedata.normalize("NFKC", text)
        text = text.translate(translation_table)
        text = text.encode("ascii", "ignore").decode("ascii")

        return text

    def split_into_pages(self, text: str) -> List[str]:
        return text.split(self.document_manager.PAGE_SEPARATOR)

    def execute(self) -> None:
        for file in self.document_manager.files:
            self.execute_by_document(file)

    def execute_by_document(self, document: Document) -> None:
        if document.pipeline_executed:
            return

        document.clean = self.clear(document.content)
        document.normalized = self.normalize(document.clean)
        document.pages = self.split_into_pages(document.normalized)

        if document.clean and document.normalized:
            dao = DocumentoDao()
            document.pipeline_executed = True
            dao.update(document.id, document.to_dict())
