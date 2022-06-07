from os import path
from typing import List


class FileHelper:
    @staticmethod
    def isFile(filePath: str) -> bool:
        return path.isfile(filePath)

    @staticmethod
    def isDirectory(directoryPath: str) -> bool:
        return path.isdir(directoryPath)

    @staticmethod
    def getDirectoriesFromList(pathList: List[str]) -> List[str]:
        resultList = []
        for eachPath in pathList:
            if FileHelper.isDirectory(eachPath):
                resultList.append(eachPath)
        return resultList

    @staticmethod
    def getFilesFromList(pathList: List[str]) -> List[str]:
        resultList = []
        for eachPath in pathList:
            if FileHelper.isFile(eachPath):
                resultList.append(eachPath)
        return resultList
