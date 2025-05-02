from typing import List


class Document:
    def __init__(self, name: str, path: str):
        self.name: str = name
        self.path: str = path
        self.content: str = ""
        self.clean: str = ""
        self.normalized: str = ""
        self.tokens: List[str] = []
        self.pipeline_executed: bool = False
        self.information_extracted: bool = False
