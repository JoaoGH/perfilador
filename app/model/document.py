import hashlib
import json
from typing import List


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

    def calculate_hash(self) -> None:
        self.hash = hashlib.sha256(self.content.encode()).hexdigest()

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
        }

        return dictionary
