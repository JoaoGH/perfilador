import warnings
from pathlib import Path
from typing import List, Optional

import PyPDF2

from app.document import Document

class DocumentManager:
    def __init__(self, pdf_folder: str = "resources/pdf"):
        self.files: List[Document] = []
        self.pdf_folder: Path = Path(pdf_folder)

        if not self.pdf_folder.exists():
            raise FileNotFoundError(f"Diretório não encontrado '{self.pdf_folder}'")

    def load_pdf(self) -> None:
        pdf_files = list(self.pdf_folder.glob("*.pdf"))

        if not pdf_files:
            print(f"Nenhum arquivo PDF encontrado no diretório '{self.pdf_folder}'.")
            return

        for pdf_file in pdf_files:
            file_name = pdf_file.name
            if file_name in self.files:
                continue

            try:
                doc = Document(file_name, str(pdf_file))
                doc.content = self.read_file(pdf_file)
                self.files.append(doc)
            except Exception as e:
                print(f"Erro ao carregar o arquivo '{file_name}': {str(e)}")

    def read_file(self, path: Path) -> Optional[str]:
        content = []

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with open(path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)

                    for page in reader.pages:
                        text = page.extractText() or ""
                        if text.strip():
                            content.append(text)
        except Exception as e:
            print(f"Erro ao ler '{path.name}': {str(e)}")
            return None

        return "\n".join(content) if content else None

    def list_documents(self) -> None:
        for idx, doc in enumerate(self.files):
            status = "✓" if doc.pipeline_executed else "⌛"
            print(f"[{(idx+1):02d}] {status} - {doc.name}")
