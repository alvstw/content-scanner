from typing import Callable, Any

from src.constant.fileType import FileType, RpaFileType, OtherFileType
from src.engine.search_engine.file_search_engine import FileSearchEngine
from src.engine.search_engine.plain_text_file_search_engine import PlainTextFileSearchEngine
from src.exception.search_engine_exception import NotSupportedFileException


class SearchDispatcher:
    _searchEngines: dict[str, Callable]

    def __init__(self):
        self._searchEngines = {
            RpaFileType.name: PlainTextFileSearchEngine,
            OtherFileType.name: PlainTextFileSearchEngine,
        }

    def fileContains(self, fileType: FileType, filePath: str, searchValue: Any, caseSensitive: bool = True):
        if fileType.name not in self._searchEngines:
            raise NotSupportedFileException

        # noinspection PyTypeChecker
        fileSearchEngineClass: FileSearchEngine = self._searchEngines[fileType.name]

        fileSearchEngine = fileSearchEngineClass()
        fileSearchEngine.open(path=filePath, caseSensitive=caseSensitive)
        return fileSearchEngine.contains(searchValue)
