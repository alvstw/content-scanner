from typing import List

from src import context
from src.constant.fileType import AllFileType, OtherFileType
from src.context import threadManager
from src.context_manager.progress_bar_context_manager import ProgressBarContextManager
from src.engine.search_dispatcher import SearchDispatcher
from src.exception.file_exception import PathNotFoundException, PermissionDeniedException
from src.extension_helper import ExtensionHelper
from src.library.helper.file_helper import FileHelper
from src.library.helper.list_helper import ListHelper
from src.thread_manager import ThreadType


class SearchService:
    threadCount: int
    searchDispatcher: SearchDispatcher

    def __init__(self, threadCount: int = 10):
        self.threadCount = threadCount

        self.searchDispatcher = SearchDispatcher()

    def searchKeyword(self, searchPath: str, keyword: str, scanFileTypes: List[str] = None, depth: int = None,
                      caseSensitive: bool = True) -> List[str]:
        matchedList: List[str] = []

        # Compile list of extensions to search
        if ExtensionHelper.hasType(scanFileTypes, AllFileType):
            searchExtension = None
        else:
            searchExtension = ExtensionHelper.getExtensionsFromNames(scanFileTypes)
            if ExtensionHelper.hasType(scanFileTypes, OtherFileType):
                searchExtension.append('')
            searchExtension = searchExtension if len(searchExtension) != 0 else None

        # Perform discovery
        fileList = SearchService.findFromDirectory(
            searchPath, searchDepth=depth, searchExtension=searchExtension, threadCount=self.threadCount
        )
        # Perform search
        with ProgressBarContextManager(unit=' file', total=len(fileList)) as pbar:
            pbar.setDescription('Reading')
            exitEvent = threadManager.ping(lambda: pbar.refresh())
            # split the files for threads to run
            partList = ListHelper.split(fileList, self.threadCount)
            for part in partList:
                threadManager.execute(
                    self._readFileThread,
                    threadType=ThreadType.READ_FILE_THREAD,
                    args=(
                        part,
                        keyword, caseSensitive, pbar,
                        matchedList,),
                    blockingLock=True
                )
            threadManager.joinThreads(ThreadType.READ_FILE_THREAD)
            pbar.setDescription('Read')
            exitEvent.set()
        context.messageHelper.print(f'Search completed ({len(matchedList)} found)')
        return matchedList

    @staticmethod
    def findFromDirectory(
            findPath: str,
            searchExtension: List[str] = None,
            excludedExtension: List[str] = None,
            searchDepth: [int, None] = None,
            threadCount: int = 10
    ) -> List[str]:
        unlimitedDepth = True if not isinstance(searchDepth, int) else False
        findPath = FileHelper.getAbsolutePath(findPath)
        startingDepth = FileHelper.getDepth(findPath)
        allowedDepth = 0 if unlimitedDepth else searchDepth + startingDepth

        resultList: List[str] = []
        pendingDirectoryList: List[str] = [findPath]

        with ProgressBarContextManager(unit=' directory') as pbar:
            pbar.setDescription('Discovering')
            exitEvent = threadManager.ping(lambda: pbar.refresh())
            for _ in range(threadCount):
                threadManager.execute(
                    SearchService._discoverPathThread,
                    threadType=ThreadType.DISCOVERY_THREAD,
                    args=(
                        searchExtension, excludedExtension,
                        unlimitedDepth, allowedDepth, pendingDirectoryList, pbar,
                        resultList
                    ),
                    blockingLock=True
                )
            while True:
                threadManager.joinThreads(ThreadType.DISCOVERY_THREAD)
                if len(pendingDirectoryList) == 0:
                    break
            pbar.setDescription('Discovered')
            context.messageHelper.log(f'Discovered {pbar.getCount()}')
            exitEvent.set()

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

    @staticmethod
    def _discoverPathThread(
            searchExtension: List[str], excludedExtension: List[str],
            unlimitedDepth: bool, allowedDepth: int, pendingDirectoryList: List[str], pbar: ProgressBarContextManager,
            filteredFileList: List[str]
    ) -> None:
        while len(pendingDirectoryList) != 0:
            currentDirectory = pendingDirectoryList.pop(0)
            currentDepth = FileHelper.getDepth(currentDirectory)

            context.messageHelper.print(f'Discovering: {currentDirectory}')

            pbar.update(1)  # scan one directory
            # Look for the directory from the current directory and add them to pendingForDiscoveryList
            try:
                fileOnlyList = SearchService.listDirectory(currentDirectory, excludeDirectory=True)
                directoryOnlyList = SearchService.listDirectory(currentDirectory, excludeFile=True)
            except PathNotFoundException:
                context.messageHelper.print(f'File not found: {currentDirectory}')
                return
            except PermissionDeniedException:
                context.messageHelper.print(f'Permission denied: {currentDirectory}')
                return

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
                filteredFileList.append(file)

    def _readFileThread(
            self, filePathList: List[str],
            searchValue: str, caseSensitive: bool, pbar: ProgressBarContextManager,
            matchedList: List):
        for filePath in filePathList:
            pbar.update(1)
            context.messageHelper.print(f'Reading: {filePath}')
            fileType = ExtensionHelper.getFileTypeByPath(filePath)
            if fileType is None:
                # Can't find file type associated with the extension
                continue
            if self.searchDispatcher.fileContains(
                    filePath=filePath, fileType=fileType, searchValue=searchValue, caseSensitive=caseSensitive
            ):
                matchedList.append(filePath)
