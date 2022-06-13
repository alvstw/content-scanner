from typing import List

import pandas as pd

from scanner.src.constant.general import FilePath
from scanner.src.library.helper.file_helper import FileHelper
from scanner.src.library.helper.time_helper import TimeHelper


class ReportService:
    def __init__(self):
        FileHelper.createDirectoryIfNotExist(FilePath.DATA)

    def writeCSV(self, matchedList: List[str]) -> str:
        dataDict = {
            'Matched File': matchedList
        }
        df = pd.DataFrame(data=dataDict)
        filePath = FileHelper.joinPath(FilePath.DATA, TimeHelper.formatTime(fmt='%Y-%m-%d %H%M'))
        filePath = f'{filePath}.csv'
        df.to_csv(filePath)

        return filePath
