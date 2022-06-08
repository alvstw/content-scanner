import os
from os import path
from typing import List

from src.exception.file_exception import PathNotFoundException, PermissionDeniedException


class FileHelper:
    @staticmethod
    def isFile(filePath: str) -> bool:
        return path.isfile(filePath)

    @staticmethod
    def isDirectory(directoryPath: str) -> bool:
        return path.isdir(directoryPath)

    @staticmethod
    def listDirectory(directoryPath: str, returnFullPath: bool = False) -> List[str]:
        try:
            rs = os.listdir(directoryPath)
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
        return fileExtension

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