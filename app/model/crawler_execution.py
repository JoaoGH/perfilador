from datetime import datetime
from typing import Optional


class CrawlerExecution:
    def __init__(self):
        self.id = None
        self.search_query: Optional[str] = None
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.total_arquivos: int = 0
        self.successful_downloads: int = 0
        self.failed_downloads: int = 0
        self.duration_seconds: Optional[float] = None

    @staticmethod
    def get_table_name() -> str:
        return "crawler_execucoes"

    def to_dict(self) -> dict:
        dictionary = {
            "search_query": self.search_query,
            "start_time": self.start_time.isoformat() if self.start_time is not None else None,
            "end_time": self.end_time.isoformat() if self.end_time is not None else None,
            "total_arquivos": self.total_arquivos,
            "successful_downloads": self.successful_downloads,
            "failed_downloads": self.failed_downloads,
            "duration_seconds": self.duration_seconds,
        }

        return dictionary

    def calculate_duration(self):
        if self.start_time and self.end_time:
            self.duration_seconds = (self.end_time - self.start_time).total_seconds()
