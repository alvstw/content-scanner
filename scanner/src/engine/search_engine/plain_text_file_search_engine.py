from typing import Any

from scanner.src import context
from scanner.src.engine.search_engine.file_search_engine import FileSearchEngine


class PlainTextFileSearchEngine(FileSearchEngine):
    def open(self, path: str, caseSensitive: bool = True) -> bool:
        self.caseSensitive = caseSensitive
        # noinspection PyBroadException
        try:
            with open(path, 'r', encoding='utf8') as file:
                self.content = file.read()
                return True
        except Exception as err:
            context.messageHelper.log(f'Failed to read {path}: {err}')
            return False

    def contains(self, searchString: Any) -> bool:
        # noinspection PyBroadException
        try:
            content = str(self.content)
            searchString = str(searchString)
            # handle case-sensitive
            if not self.caseSensitive:
                content = content.lower()
                searchString = searchString.lower()
            # perform search
            if searchString in content:
                return True
            return False
        except Exception:
            return False
