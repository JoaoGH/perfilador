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
        """Executa todas as operações de limpeza básica do texto"""

        if not text:
            return ""

        text = text.strip().lower()
        text = re.sub(r"-[\r\n\t]+", "", text)
        text = re.sub(r"[\r\n\t]+", " ", text)

        for it in ("\.\.", "__", ": ", ":_", ":\."):
            regex = r"(?<=[a-z])(" + it + ")(?=[a-z])"
            text = re.sub(regex, " ", text)

        text = re.sub(r"\s+", " ", text)

        return text

    def normalize(self, text: str) -> str:
        """Executa a normalização do texto"""

        if not text:
            return ""

        # Tabela de tradução
        translation_table = str.maketrans(
            'áàâãäéèêëíìîïóòôõöúùûüç',
            'aaaaaeeeeiiiiooooouuuuc'
        )

        text = unicodedata.normalize("NFKC", text)
        text = text.translate(translation_table)
        text = text.encode("ascii", "ignore").decode("ascii")
        text = re.sub(r"[^\w\s]", "", text)
        return text

    def tokenize(self, text: str) -> list:
        """Tokeniza o conteudo usando NLTK"""

        if not text:
            return []

        try:
            return nltk.word_tokenize(text)
        except Exception as e:
            print(f"Erro ao tokenizar: {str(e)}")
            return []

    def execute(self) -> None:
        for file in self.document_manager.files:
            self.execute_by_document(file)

    def execute_by_document(self, document: Document) -> None:
        if document.pipeline_executed:
            return

        document.clean = self.clear(document.content)
        document.normalized = self.normalize(document.clean)
        document.tokens = self.tokenize(document.normalized)

        if document.clean and document.normalized and document.tokens:
            document.pipeline_executed = True
