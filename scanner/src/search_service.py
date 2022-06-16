import re
from time import sleep
from typing import List

from scanner.src import context
from scanner.src.constant.fileType import AllFileType, OtherFileType
from scanner.src.context import threadManager, discoveryPhaseThreadCount, readingPhaseThreadCount, \
    discoveryPhaseIdleLock, discoveryPhaseExitEvent
from scanner.src.context_manager.progress_bar_context_manager import ProgressBarContextManager
from scanner.src.engine.search_dispatcher import SearchDispatcher
from scanner.src.exception.app_exception import UnexpectedException
from scanner.src.exception.file_exception import PathNotFoundException, PermissionDeniedException
from scanner.src.extension_helper import ExtensionHelper
from scanner.src.library.helper.file_helper import FileHelper
from scanner.src.library.helper.list_helper import ListHelper
from scanner.src.thread_manager import ThreadType


class SearchService:
    searchDispatcher: SearchDispatcher

    def __init__(self):
        self.searchDispatcher = SearchDispatcher()

    def searchKeyword(self, searchPath: str, keyword: str, scanFileTypes: List[str] = None,
                      exclusionRule: [str, None] = None, depth: int = None,
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
            searchPath, searchDepth=depth, searchExtension=searchExtension,
            exclusionRule=exclusionRule, threadCount=discoveryPhaseThreadCount
        )
        # Perform search
        with ProgressBarContextManager(unit=' file', total=len(fileList)) as pbar:
            pbar.setDescription('Reading')
            # split the files for threads to run
            partList = ListHelper.split(fileList, readingPhaseThreadCount)
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
        context.messageHelper.print(f'Search completed ({len(matchedList)} found)')
        return matchedList

    @staticmethod
    def findFromDirectory(
            findPath: str,
            searchExtension: List[str] = None,
            excludedExtension: List[str] = None,
            exclusionRule: str = None,
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
            for _ in range(threadCount):
                threadManager.execute(
                    SearchService._discoverPathThread,
                    threadType=ThreadType.DISCOVERY_THREAD,
                    args=(
                        searchExtension, excludedExtension, exclusionRule,
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

        return resultList

    @staticmethod
    def listDirectory(directoryPath: str, excludeDirectory: bool = False, excludeFile: bool = False) -> List[str]:
        try:
            directoryContent = FileHelper.listDirectory(directoryPath, returnFullPath=True)
        except PathNotFoundException:
            raise PathNotFoundException
        except PermissionDeniedException:
            raise PermissionDeniedException
        except UnexpectedException:
            raise UnexpectedException

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
            searchExtension: List[str], excludedExtension: List[str], exclusionRule: str,
            unlimitedDepth: bool, allowedDepth: int, pendingDirectoryList: List[str], pbar: ProgressBarContextManager,
            filteredFileList: List[str]
    ) -> None:
        idleLockedThread: bool = False
        idleCheckDelay: int = 5
        while True:
            if discoveryPhaseExitEvent.is_set():
                return
            if len(pendingDirectoryList) == 0:
                if idleLockedThread:
                    sleep(idleCheckDelay)
                    continue
                if discoveryPhaseIdleLock.acquire(blocking=False):
                    idleLockedThread = True
                    context.messageHelper.log(f'The thread is idle')
                    continue
                else:
                    context.messageHelper.log(f'An exit event is triggered')
                    discoveryPhaseExitEvent.set()
                    return
            else:
                if idleLockedThread:
                    idleLockedThread = False
                    discoveryPhaseIdleLock.release()

            currentDirectory = pendingDirectoryList.pop(0)
            currentDepth = FileHelper.getDepth(currentDirectory)

            # check against excluded keyword
            if isinstance(exclusionRule, str):
                try:
                    pbar.setDescription(f'Discovering (Exclusion Rule: Enabled)')
                    nDirectoryName = FileHelper.getDirectoryName(currentDirectory)
                    if re.match(exclusionRule, nDirectoryName):
                        context.messageHelper.print(f'Excluded directory: {currentDirectory}')
                        pbar.update(1)  # skip one directory
                        continue
                except re.error:
                    exclusionRule = None
                    pbar.setDescription(f'Discovering (Exclusion Rule: Disabled)')
                    context.messageHelper.print('Exclusion rule is disabled due to error.')

            context.messageHelper.print(f'Discovering: {currentDirectory}')

            pbar.update(1)  # scan one directory
            # Look for the directory from the current directory and add them to pendingForDiscoveryList
            try:
                fileOnlyList = SearchService.listDirectory(currentDirectory, excludeDirectory=True)
                directoryOnlyList = SearchService.listDirectory(currentDirectory, excludeFile=True)
            except PathNotFoundException:
                context.messageHelper.print(f'File not found: {currentDirectory}')
                continue
            except PermissionDeniedException:
                context.messageHelper.print(f'Permission denied: {currentDirectory}')
                continue
            except UnexpectedException:
                context.messageHelper.print(f'Unexpected error: {currentDirectory}')
                continue

                # if next level is within the allowed depth
            if unlimitedDepth or currentDepth + 1 <= allowedDepth:
                pendingDirectoryList.extend(directoryOnlyList)
                pbar.addTotal(len(directoryOnlyList))

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
                pbar.setPostfix(f'{len(filteredFileList)} files pending')

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
                context.messageHelper.print(f'Found the keyword in: {filePath}')
                matchedList.append(filePath)
                pbar.setPostfix(f'{len(matchedList)} files found')
