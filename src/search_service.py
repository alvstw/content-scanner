from typing import List

from src import context
from src.constant.fileType import FileType
from src.context_manager.progress_bar_context_manager import ProgressBarContextManager
from src.engine.search_dispatcher import SearchDispatcher
from src.exception.file_exception import PathNotFoundException, PermissionDeniedException
from src.library.helper.file_helper import FileHelper


class SearchStatus:
    NOT_DISCOVERED = 'NOT_DISCOVERED'
    TRANSVERSED = 'TRANSVERSED'


class SearchService:
    searchDispatcher: SearchDispatcher

    def __init__(self):
        self.searchDispatcher = SearchDispatcher()

    def searchKeyword(self, searchPath: str, keyword: str, depth: int = None, caseSensitive: bool = True) -> List[str]:
        matchedList: List[str] = []
        # TODO: handle search extension
        fileList = SearchService.findFromDirectory(searchPath, searchDepth=depth, searchExtension=['.xaml'])
        with ProgressBarContextManager(unit=' file', total=len(fileList)) as pbar:
            pbar.set_description('Reading')
            for file in fileList:
                pbar.update(1)
                # TODO: handle file type based on extension
                fileType = FileType.rpaFile
                if self.searchDispatcher.performSearch(
                        filePath=file, fileType=fileType, searchValue=keyword, caseSensitive=caseSensitive
                ):
                    matchedList.append(file)
            pbar.set_description('Read')
        context.messageHelper.print(f'Search completed ({len(matchedList)} found)')
        return matchedList

    @staticmethod
    def findFromDirectory(
            findPath: str,
            searchExtension: List[str] = None,
            excludedExtension: List[str] = None,
            searchDepth: [int, None] = None
    ) -> List[str]:
        unlimitedDepth = True if not isinstance(searchDepth, int) else False
        findPath = FileHelper.getAbsolutePath(findPath)
        startingDepth = FileHelper.getDepth(findPath)
        allowedDepth = 0 if unlimitedDepth else searchDepth + startingDepth

        resultList: List[str] = []
        pendingDirectoryList: List[str] = [findPath]

        with ProgressBarContextManager(unit=' directory') as pbar:
            pbar.set_description('Discovering')
            while len(pendingDirectoryList) != 0:
                currentDirectory = pendingDirectoryList.pop(0)
                currentDepth = FileHelper.getDepth(currentDirectory)

                pbar.update(1)  # scan one directory
                # Look for the directory from the current directory and add them to pendingForDiscoveryList
                try:
                    fileOnlyList = SearchService.listDirectory(currentDirectory, excludeDirectory=True)
                    directoryOnlyList = SearchService.listDirectory(currentDirectory, excludeFile=True)
                except (PathNotFoundException, PermissionDeniedException):
                    context.messageHelper.print(f'Permission denied: {currentDirectory}')
                    continue
                # if next level is within the allowed depth
                if unlimitedDepth or currentDepth + 1 <= allowedDepth:
                    pendingDirectoryList.extend(directoryOnlyList)
                    pass

                # Look for the content from the current directory
                for file in fileOnlyList:
                    extension = FileHelper.getFileExtension(file)
                    if excludedExtension is not None:
                        if extension in excludedExtension:
                            continue
                    if searchExtension is not None:
                        if extension not in searchExtension:
                            continue
                    resultList.append(file)
            pbar.set_description('Discovered')

        return resultList

    @staticmethod
    def listDirectory(directoryPath: str, excludeDirectory: bool = False, excludeFile: bool = False) -> List[str]:
        try:
            directoryContent = FileHelper.listDirectory(directoryPath, returnFullPath=True)
        except PathNotFoundException:
            raise PathNotFoundException
        except PermissionDeniedException:
            raise PermissionDeniedException

        directoryList: List[str] = []
        fileList: List[str] = []
        resultList: List[str] = []

        if not excludeDirectory:
            directoryList = FileHelper.getDirectoriesFromList(directoryContent)
        if not excludeFile:
            fileList = FileHelper.getFilesFromList(directoryContent)

        resultList.extend(directoryList)
        resultList.extend(fileList)
        return resultList
