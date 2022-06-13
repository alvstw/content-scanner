from typing import Callable, Any

from scanner.src.constant.fileType import FileType, RpaFileType, OtherFileType, ExcelFileType
from scanner.src.engine.search_engine.file_search_engine import FileSearchEngine
from scanner.src.engine.search_engine.plain_text_file_search_engine import PlainTextFileSearchEngine
from scanner.src.exception.search_engine_exception import NotSupportedFileException


class SearchDispatcher:
    _searchEngines: dict[str, Callable]

    def __init__(self):
        self._searchEngines = {
            RpaFileType.name: PlainTextFileSearchEngine,
            ExcelFileType.name: PlainTextFileSearchEngine,
            OtherFileType.name: PlainTextFileSearchEngine,
        }

    def fileContains(self, fileType: FileType, filePath: str, searchValue: Any, caseSensitive: bool = True) -> bool:
        if fileType.name not in self._searchEngines:
            raise NotSupportedFileException

        # noinspection PyTypeChecker
        fileSearchEngineClass: FileSearchEngine = self._searchEngines[fileType.name]

        fileSearchEngine = fileSearchEngineClass()
        fileSearchEngine.open(path=filePath, caseSensitive=caseSensitive)
        return fileSearchEngine.contains(searchValue)
