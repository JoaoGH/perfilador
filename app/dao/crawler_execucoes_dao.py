from datetime import datetime
from typing import Optional

from app.dao.base_dao import BaseDAO
from app.model.crawler_execution import CrawlerExecution


class CrawlerExecutionDao(BaseDAO[CrawlerExecution]):

    def __init__(self):
        super().__init__(CrawlerExecution)

    def _get_conversion_map(self) -> dict:
        return {
            'start_time': self._convert_to_datetime,
            'end_time': self._convert_to_datetime,
        }

    def _convert_to_datetime(self, value: str) -> Optional[datetime]:
        if not value:
            return None
        return datetime.fromisoformat(value) if isinstance(value, str) else value
