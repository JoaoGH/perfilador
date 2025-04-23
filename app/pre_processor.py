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

        text = re.sub(r"(?<!\s)\(", " (", text)
        text = re.sub(r"\)(?!\s)", ") ", text)

        text = re.sub(r"_", " ", text)

        text = re.sub(r"\s+", " ", text)

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

    def tokenize(self, text: str) -> list:
        """Tokeniza o conteudo usando NLTK"""

        if not text:
            return []

        try:
            regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(regex_email, text)
            protected_text = re.sub(regex_email, '||EMAIL||', text)

            content = nltk.word_tokenize(protected_text)

            email_index = 0

            for token in content:
                if token == '||EMAIL||':
                    content[content.index(token)] = emails[email_index]
                    email_index += 1

            return content
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
