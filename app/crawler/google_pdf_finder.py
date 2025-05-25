import time
from typing import List, Optional, Set

from googlesearch import search


class GooglePDFFinder:
    def __init__(self, num_results: int = 10, delay: float = 2.0):
        """
        Inicializa o buscador de PDFs no Google.

        :param num_results: Número de resultados por query
        :param delay: Atraso entre requisições (evitar bloqueio)
        """
        self.num_results = num_results
        self.delay = delay
        self.base_queries = [
            "(cpf OR rg) AND (lista OR listagem OR declaração OR declaracao)",
            "(processo OR selecao) AND (lista OR listagem OR declaração OR declaracao)",
        ]

    def search(self, custom_query: Optional[str] = None) -> List[str]:
        """
        Busca URLs de PDFs no Google baseado nas queries.

        :param custom_query: Query personalizada para adicionar às queries base
        :return: Lista de URLs de PDFs encontrados
        """

        urls: Set[str] = set()
        FILE_TYPE = " filetype:pdf"

        for base_query in self.base_queries:
            current_query = base_query
            if custom_query:
                current_query += f" AND \"{custom_query}\""
            current_query += FILE_TYPE

            try:
                print(f"Buscando: {current_query}")

                founded =  search(current_query, num_results=self.num_results)

                for url in founded:
                    if url != '' and self._is_valid_pdf_url(url):
                        urls.add(url)
                time.sleep(self.delay)
            except Exception as e:
                print(e)

        return list(urls)

    def _is_valid_pdf_url(self, url: str) -> bool:
        """Verifica se a URL aponta para um PDF"""
        return url.lower().endswith('.pdf') or 'pdf' in url.lower()

