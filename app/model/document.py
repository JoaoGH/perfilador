import hashlib
import json
import os.path
from datetime import datetime
from typing import List, Optional

from app.model.crawler_execution import CrawlerExecution


class Document:
    def __init__(self, name: str = "", path: str = ""):
        self.id = None
        self.name: str = name
        self.path: str = path
        self.content: str = ""
        self.clean: str = ""
        self.normalized: str = ""
        self.tokens: List[str] = []
        self.pipeline_executed: bool = False
        self.information_extracted: bool = False
        self.hash: str = ""
        self.crawler: CrawlerExecution = CrawlerExecution()
        self.source_url: Optional[str] = ""
        self.search_query: Optional[str] = ""
        self.download_timestamp: Optional[datetime] = None

    def calculate_hash(self, use_file_content: bool = False) -> None:
        if use_file_content and os.path.exists(self.path):
            with open(self.path, "rb") as f:
                file_content = f.read()
        else:
            file_content = self.content.encode()

        self.hash = hashlib.sha256(file_content).hexdigest()

    @staticmethod
    def get_table_name() -> str:
        return "documentos"

    def to_dict(self):
        dictionary = {
            "name": self.name,
            "path": self.path,
            "content": self.content,
            "clean": self.clean,
            "normalized": self.normalized,
            "tokens": json.dumps(self.tokens),
            "pipeline_executed": int(self.pipeline_executed),
            "information_extracted": int(self.information_extracted),
            "hash": self.hash,
            "crawler_execucao_id": self.crawler.id if self.crawler.id is not None else None,
            "source_url": self.source_url,
            "search_query": self.search_query,
            "download_timestamp": self.download_timestamp.isoformat() if self.download_timestamp is not None else None,
        }

        return dictionary

    def file_exists(self) -> bool:
        return os.path.exists(self.path)
