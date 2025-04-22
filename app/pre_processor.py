import re
import unicodedata
import nltk

from app.document import Document
from app.document_manager import DocumentManager


class PreProcessor:

    def __init__(self):
        # Garante que os recursos do NLTK estão disponíveis
        nltk.download('punkt', quiet=True)
        self.document_manager = DocumentManager()

    def clear(self, text: str) -> str:
        return re.sub(r"[\r\n]+", " ", text).lower()

    def normalize(self, text: str) -> str:
        text = unicodedata.normalize("NFKC", text)
        text = text.encode("ascii", "ignore").decode("utf-8")
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return text

    def tokenize(self, text: str) -> list:
        return nltk.word_tokenize(text)

    def execute(self) -> None:
        for file in self.document_manager.files:
            self.execute_by_document(file)

    def execute_by_document(self, document: Document) -> None:
        document.clean = self.clear(document.content)
        document.normalized = self.normalize(document.clean)
        document.tokenized = self.tokenize(document.normalized)
        document.pipeline_executed = True
