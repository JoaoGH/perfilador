import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.crawler.google_pdf_finder import GooglePDFFinder
from app.crawler.pdf_downloder import PDFDownloader
from app.dao.crawler_execucoes_dao import CrawlerExecutionDao
from app.dao.documentos_dao import DocumentoDao
from app.document_manager import DocumentManager
from app.model.crawler_execution import CrawlerExecution
from app.model.document import Document


class PDFCrawler:
    def __init__(self, directory: str = "resources/pdf"):
        """
        Inicializa o crawler para buscar e baixar PDFs.

        :param directory: Diretório onde os PDFs serão salvos
        """
        self.directory = directory
        self.finder = GooglePDFFinder()
        self.downloader = PDFDownloader(directory)
        self.dao = CrawlerExecutionDao()
        self.document_dao = DocumentoDao()
        self.document_manager = DocumentManager()

    def run(self, query: Optional[str] = None) -> None:
        """
        Executa o processo completo de busca e download

        :param query: Termo de busca personalizado (opcional)
        """

        execucao = CrawlerExecution()
        execucao.search_query = query.strip() if query else None
        execucao.start_time = datetime.now()
        execucao.id = self.dao.insert(execucao)

        query = execucao.search_query

        print(f"Buscando PDFs para: \"{query}\"" if query else "Buscando PDFs com queries padroes")

        success_downloaded = 0
        failed_downloaded = 0

        try:
            pdf_urls = self.finder.search(query)

            if not pdf_urls:
                print("Nenhum PDF encontrado")
                execucao.end_time = datetime.now()
                execucao.calculate_duration()
                self.dao.update(execucao.id, execucao.to_dict())
                return

            print(f"\n{len(pdf_urls)} PDFs encontrados.")

            for url, used_query in pdf_urls:
                result = self.downloader.download(url, execucao.id)
                if result['success']:
                    # criar um doc
                    doc = Document(
                        name=os.path.basename(result['file_path']),
                        path=result['file_path']
                    )
                    doc.source_url = url
                    doc.search_query = used_query
                    doc.crawler = execucao
                    doc.content = self.document_manager.read_file(Path(result['file_path']))
                    doc.calculate_hash()
                    doc.download_timestamp = result['download_timestamp']
                    if doc.file_exists() and self.document_dao.exists_by_hash(doc.hash):
                        os.remove(result['file_path'])
                        continue
                    self.document_dao.insert(doc)
                    success_downloaded += 1

                else:
                    failed_downloaded += 1

        except Exception as e:
            print(f"Erro durante busca: {e}")
        finally:
            execucao.end_time = datetime.now()
            execucao.successful_downloads = success_downloaded
            execucao.failed_downloads = failed_downloaded
            execucao.calculate_duration()

            self.dao.update(execucao.id, execucao.to_dict())

        print(f"{execucao.successful_downloads} arquivo(s) salvo(s) conforme execucao.")
