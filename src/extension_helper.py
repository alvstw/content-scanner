from typing import List, Any

from src.constant.fileType import fileTypeList, FileType, OtherFileType
from src.library.helper.file_helper import FileHelper


class ExtensionHelper:
    @staticmethod
    def getFileType(extension: str) -> [FileType, None]:
        fileType: FileType
        if extension == '':
            return OtherFileType
        for fileType in fileTypeList:
            for fileTypeExtension in fileType.extension:
                if fileTypeExtension == extension:
                    return fileType
        return None

    @staticmethod
    def getFileTypeByPath(filePath: str) -> [FileType, None]:
        extension = FileHelper.getFileExtension(filePath)
        return ExtensionHelper.getFileType(extension)

    @staticmethod
    def getFileTypeExtension(name: str) -> [List[str], None]:
        fileType: FileType
        for fileType in fileTypeList:
            if fileType.name == name:
                return fileType.extension
        return None

    @staticmethod
    def hasType(names: List[str], fileType: [FileType, Any]) -> bool:
        for name in names:
            if name == fileType.name:
                return True
        return False

    @staticmethod
    def getExtensionsFromNames(names: List[str]) -> List[str]:
        rs = []
        for name in names:
            extensions = ExtensionHelper.getFileTypeExtension(name)
            if extensions is not None:
                rs.extend(extensions)
        return rs
