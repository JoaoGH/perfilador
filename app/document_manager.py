import re
import sys
import time
from pathlib import Path
from threading import Event, Thread
from typing import List, Optional
import fitz

from app.dao.documentos_dao import DocumentoDao
from app.model.document import Document

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

    def load_from_database(self) -> None:
        print("Iniciar leitura de arquivos do banco de dados.")

        try:
            dao = DocumentoDao()
            documents = dao.list()
            for document in documents:
                if document.file_exists():
                    self.files.append(document)
                else:
                    dao.remove(document.id)
        except Exception as e:
            print(e)

        print("Leitura finalizada.")
        return

    def load_pdf(self) -> None:
        """Carrega todos os PDFs do diretório especificado com barra de progresso."""
        pdf_files = list(self.pdf_folder.glob("*.pdf"))

        pdf_files = sorted(pdf_files, key=lambda x: x.name)

        if not pdf_files:
            print(f"Nenhum arquivo PDF encontrado no diretório '{self.pdf_folder}'.")
            return

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
            dao = DocumentoDao()

            for i, pdf_file in enumerate(pdf_files):
                file_name = pdf_file.name

                try:
                    doc = Document(file_name, str(pdf_file))
                    doc.content = self.read_file(pdf_file)
                    doc.calculate_hash()
                    if dao.exists_by_hash(doc.hash):
                        continue
                    doc.id = dao.insert(doc)
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
        """Extrai conteudo do PDF"""

        try:
            text = ""
            with fitz.open(path) as doc:
                for page in doc:
                    text += page.get_text("text") + "\n"

            text = self.remover_anuncios(text)

            return text

        except Exception as e:
            print(f"Erro ao ler {path}: {str(e)}")
            return ""

    def list_documents(self) -> None:
        if len(self.files) == 0:
            return

        print(f"{'ID':<4} | {'Pipeline':<8} | {'Information':<11} | Nome Documento")
        print("-"*48)
        for idx, doc in enumerate(self.files, start=1):
            status_pipeline = "✓" if doc.pipeline_executed else "⌛"
            status_information = "✓" if doc.information_extracted else "⌛"
            print(f"{idx:>4} | {status_pipeline:^8} | {status_information:^11} | {doc.name}")

    def remover_anuncios(self, text) -> str:
        """Remover anuncio do editor de PDF gratuito usado para preencher os arquivos"""

        anuncio = r"(P\nD\nF\n-\nX\nC\nh\na\nn\ng\ne\nE\nd\ni\nt\no\nr\nw\nw\nw\n.\np\nd\nf\n-\nx\nc\nh\na\nn\ng\ne\n.\nc\no\nm)+"
        text = re.sub(anuncio, "", text)
        text = re.sub(r"(Click to BUY NOW!)+", "", text)
        return text
