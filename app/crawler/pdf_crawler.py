import os
from datetime import datetime
from typing import Optional

from app.crawler.google_pdf_finder import GooglePDFFinder
from app.crawler.pdf_downloder import PDFDownloader
from app.dao.crawler_execucoes_dao import CrawlerExecutionDao
from app.dao.documentos_dao import DocumentoDao
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
        self.stats = {
            'success': 0,
            'failed': 0,
            'total': 0,
            'start_time': None,
            'end_time': None
        }

    def run(self, query: Optional[str] = None) -> None:
        """
        Executa o processo completo de busca e download

        :param query: Termo de busca personalizado (opcional)
        """

        execucao = CrawlerExecution()
        execucao.search_query = query.strip() if query else None
        execucao.start_time = datetime.now()
        execucao.id = self.dao.insert(execucao)

        self.stats['start_time'] = execucao.start_time
        query = execucao.search_query

        print(f"Buscando PDFs para: \"{query}\"" if query else "Buscando PDFs com queries padroes")

        try:
            pdf_urls = self.finder.search(query)
            self.stats['total'] = len(pdf_urls)

            if not pdf_urls:
                print("Nenhum PDF encontrado")
                execucao.end_time = datetime.now()
                execucao.calculate_duration()
                self.dao.update(execucao.id, execucao.to_dict())
                return

            print(f"\n{self.stats['total']} PDFs encontrados.")

            for url in pdf_urls:
                result = self.downloader.download(url, execucao.id)
                if result['success']:
                    self.stats['success'] += 1
                    # criar um doc
                    doc = Document(
                        name=os.path.basename(result['file_path']),
                        path=result['file_path']
                    )
                    doc.source_url = url
                    doc.search_query = query
                    doc.crawler = execucao
                    doc.calculate_hash(use_file_content=True)
                    self.document_dao.insert(doc)

                else:
                    self.stats['failed'] += 1

        except Exception as e:
            print(f"Erro durante busca: {e}")
        finally:
            execucao.end_time = datetime.now()
            execucao.successful_downloads = self.stats['success']
            execucao.failed_downloads = self.stats['failed']
            execucao.calculate_duration()

            self.dao.update(execucao.id, execucao.to_dict())
            self.stats['end_time'] = execucao.end_time


    def _print_report(self):
        duration = self.stats['end_time'] - self.stats['start_time']
        print("\n=== Relatório ===")
        print(f"Tempo total: {duration.total_seconds():.2f} segundos")
        print(f"Total de PDFs encontrados: {self.stats['total']}")
        print(f"Downloads bem-sucedidos: {self.stats['success']}")
        print(f"Downloads falhos: {self.stats['failed']}")
        if self.stats['total'] > 0:
            success_rate = (self.stats['success'] / self.stats['total']) * 100
            print(f"Taxa de sucesso: {success_rate:.1f}%")

