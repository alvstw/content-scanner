from typing import Callable, Any

from src.constant.fileType import FileType
from src.engine.search_engine.file_search_engine import FileSearchEngine
from src.engine.search_engine.plain_text_file_search_engine import PlainTextFileSearchEngine
from src.exception.search_engine_exception import NotSupportedFileException


class SearchDispatcher:
    _searchEngines: dict[str, Callable]

    def __init__(self):
        self._searchEngines = {
            FileType.rpaFile: PlainTextFileSearchEngine,
            FileType.otherFIle: PlainTextFileSearchEngine,
        }

    def performSearch(self, fileType: str, filePath: str, searchValue: Any, caseSensitive: bool = True):
        if fileType not in self._searchEngines:
            raise NotSupportedFileException

        # noinspection PyTypeChecker
        fileSearchEngineClass: FileSearchEngine = self._searchEngines[fileType]

        fileSearchEngine = fileSearchEngineClass()
        fileSearchEngine.open(path=filePath, caseSensitive=caseSensitive)
        return fileSearchEngine.contains(searchValue)
