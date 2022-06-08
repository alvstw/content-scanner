import os
from os import path
from typing import List

from setuptools import unicode_utils

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

    @staticmethod
    def isSafePath(pathName):
        enc_warn = "'%s' not %s encodable -- skipping"

        # To avoid accidental trans-codings errors, first to unicode
        u_path = unicode_utils.filesys_decode(pathName)
        if u_path is None:
            # log.warn("'%s' in unexpected encoding -- skipping" % path)
            return False

        # Must ensure utf-8 encodability
        utf8_path = unicode_utils.try_encode(u_path, "utf-8")
        if utf8_path is None:
            # log.warn(enc_warn, path, 'utf-8')
            return False

        try:
            # accept is either way checks out
            if os.path.exists(u_path) or os.path.exists(utf8_path):
                return True
        # this will catch any encode errors decoding u_path
        except UnicodeEncodeError:
            return False
            # log.warn(enc_warn, path, sys.getfilesystemencoding())
