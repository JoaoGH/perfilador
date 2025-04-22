import sys
import time
import warnings
from pathlib import Path
from threading import Event, Thread
from typing import List, Optional

import PyPDF2

from app.document import Document

class DocumentManager:
    _instance = None
    _initialized = False

    def __new__(cls, pdf_folder: str = "resources/pdf"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, pdf_folder: str = "resources/pdf"):
        if not self._initialized:
            self.files: List[Document] = []
            self.pdf_folder: Path = Path(pdf_folder)
            self._initialized = True

            if not self.pdf_folder.exists():
                raise FileNotFoundError(f"Diretório não encontrado '{self.pdf_folder}'")

    def load_pdf(self) -> None:
        """Carrega todos os PDFs do diretório especificado com barra de progresso."""
        pdf_files = list(self.pdf_folder.glob("*.pdf"))

        if not pdf_files:
            print(f"Nenhum arquivo PDF encontrado no diretório '{self.pdf_folder}'.")
            return

        loaded_files = {doc.name for doc in self.files}
        stop_loading = Event()
        progress = {'current': 0, 'total': len(pdf_files)}

        # Thread para mostrar barra de progresso
        def progress_bar():
            while not stop_loading.is_set() and progress['current'] < progress['total']:
                percent = int(100 * progress['current'] / progress['total'])
                bar = '█' * int(percent / 2) + '-' * (50 - int(percent / 2))
                sys.stdout.write(f"\r[{bar}] {percent}% - {progress['current']}/{progress['total']}")
                sys.stdout.flush()
                time.sleep(0.1)

        print(f"Carregando {progress['total']} arquivos:")
        loader = Thread(target=progress_bar)
        loader.start()

        try:
            new_files_count = 0
            for i, pdf_file in enumerate(pdf_files):
                file_name = pdf_file.name
                if file_name in loaded_files:
                    continue

                try:
                    doc = Document(file_name, str(pdf_file))
                    doc.content = self.read_file(pdf_file)
                    self.files.append(doc)
                    new_files_count += 1
                except Exception as e:
                    print(f"Erro ao carregar o arquivo '{file_name}': {str(e)}")

                progress['current'] += 1

            stop_loading.set()
            loader.join()
            sys.stdout.write("\r[██████████████████████████████████████████████████] 100%\n")
            if new_files_count > 0:
                print(f"Carregados {new_files_count} novos arquivos PDF")
            else:
                print("Nenhum novo arquivo PDF para carregar")
        except Exception as e:
            stop_loading.set()
            loader.join()
            print(f"Erro durante o carregamento: {str(e)}")

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
