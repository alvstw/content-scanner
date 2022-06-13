from typing import Any


class FileSearchEngine:
    content: Any
    caseSensitive: bool

    def open(self, path: str, caseSensitive: bool = True) -> bool:
        raise NotImplemented

    def contains(self, value: Any) -> bool:
        raise NotImplemented

    def getContent(self) -> Any:
        raise NotImplemented
