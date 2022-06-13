from typing import List


class FileType:
    name: str
    extension: List[str]


class AllFileType(FileType):
    name = 'All Files'
    extension = []


class OtherFileType(FileType):
    name = 'Other Files (files without extension)'
    extension = ['']


class RpaFileType(FileType):
    name = 'RPA File'
    extension = ['.xaml']


class ExcelFileType(FileType):
    name = 'Excel File'
    extension = ['.xls', '.xlsx']


fileTypeList = [AllFileType, OtherFileType, RpaFileType, ExcelFileType]
