import os
import time
from datetime import datetime
from typing import Dict
from urllib.parse import urlparse

import requests


class PDFDownloader:
    def __init__(self, directory: str = "resources/pdf"):
        """
        Inicializa o downloader de PDFs.

        :param directory: Diretório onde os PDFs serão salvos
        """
        self.directory = directory
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def _generate_filename(self, execucao_id: int) -> str:
        return f"{execucao_id}_{int(time.time())}.pdf"

    def download(self, url: str, execucao_id: int) -> Dict:
        """
        Baixa um arquivo PDF da URL fornecida.

        :param url: URL do PDF a ser baixado
        :return: Dicionário com resultado do download
        """
        result = {
            'success': False,
            'url': url,
            'file_path': None,
            'error': None
        }

        try:
            if not self._is_valid_pdf_url(url):
                result['error'] = "URL não parece ser um PDF"
                return result

            # faz a request
            response = self.session.get(url, stream=True, timeout=15)
            response.raise_for_status()

            # verifica o content-type
            content_type = response.headers.get('Content-Type', '').lower()
            if 'pdf' not in content_type:
                result['error'] = f"Content-Type inválido: {content_type}"
                return result

            # cria o nome do arquivo
            filename = self._generate_filename(execucao_id)
            filepath = os.path.join(self.directory, filename)

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                result.update({
                    'success': True,
                    'file_path': filepath,
                    'file_size': os.path.getsize(filepath)
                })
                result['download_timestamp'] = datetime.fromtimestamp(time.time())
            else:
                result['error'] = "Arquivo vazio ou não foi salvo corretamente"

        except requests.exceptions.RequestException as e:
            result['error'] = f"Erro na requisição: {str(e)}"
        except IOError as e:
            result['error'] = f"Erro ao salvar arquivo: {str(e)}"
        except Exception as e:
            result['error'] = f"Erro inesperado: {str(e)}"

        return result

    def _is_valid_pdf_url(self, url: str) -> bool:
        """Verifica se a URL parece ser um PDF"""
        parsed = urlparse(url)
        return url.lower().endswith('.pdf') or 'pdf' in parsed.path.lower() or 'pdf' in parsed.query.lower()