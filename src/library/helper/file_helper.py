import os
from functools import lru_cache
from os import path
from typing import List

from src.exception.file_exception import PathNotFoundException, PermissionDeniedException


class FileHelper:
    @staticmethod
    @lru_cache(maxsize=16)
    def isFile(filePath: str) -> bool:
        return path.isfile(filePath)

    @staticmethod
    @lru_cache(maxsize=16)
    def isDirectory(directoryPath: str) -> bool:
        return path.isdir(directoryPath)

    @staticmethod
    @lru_cache(maxsize=16)
    def listDirectory(directoryPath: str, returnFullPath: bool = False) -> List[str]:
        try:
            rs: List[str] = []
            for root, dirs, files in FileHelper.walkDirectory(directoryPath):
                for name in files:
                    rs.append(os.path.join(root, name))
                for name in dirs:
                    rs.append(os.path.join(root, name))

            if returnFullPath:
                fullPath = FileHelper.getAbsolutePath(directoryPath)
                for n in range(len(rs)):
                    rs[n] = os.path.join(fullPath, rs[n])
            return rs
        except FileNotFoundError:
            raise PathNotFoundException
        except PermissionError:
            raise PermissionDeniedException

    @staticmethod
    def walkDirectory(directoryPath: str, level: int = 1):
        directoryPath = directoryPath.rstrip(os.path.sep)
        assert os.path.isdir(directoryPath)
        num_sep = directoryPath.count(os.path.sep)
        for root, dirs, files in os.walk(directoryPath):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    @staticmethod
    def getDirectoriesFromList(pathList: List[str]) -> List[str]:
        """
        check every file from the input to determine if it's a directory, return a list that only contains directory
        :param pathList:
        :return directoryList:
        """
        directoryList = []
        for eachPath in pathList:
            if FileHelper.isDirectory(eachPath):
                directoryList.append(eachPath)
        return directoryList

    @staticmethod
    def getFilesFromList(pathList: List[str]) -> List[str]:
        """
        check every file from the input to determine if it's a file, return a list that only contains files
        :param pathList:
        :return fileList:
        """
        fileList = []
        for eachPath in pathList:
            if FileHelper.isFile(eachPath):
                fileList.append(eachPath)
        return fileList

    @staticmethod
    def getFileExtension(filePath: str) -> str:
        _, fileExtension = os.path.splitext(filePath)
        return fileExtension.lower()

    @staticmethod
    def getAbsolutePath(relativePath: str) -> str:
        return os.path.abspath(relativePath)

    @staticmethod
    def getDepth(filePath: str) -> int:
        return len(filePath.split(os.sep))

    @staticmethod
    def joinPath(*args) -> str:
        return os.path.join(*args)

    @staticmethod
    def createDirectoryIfNotExist(folderPath: str):
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
