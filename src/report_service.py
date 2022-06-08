from typing import List

import pandas as pd

from src.constant.general import FilePath
from src.library.helper.file_helper import FileHelper
from src.library.helper.time_helper import TimeHelper


class ReportService:
    def __init__(self):
        FileHelper.createDirectoryIfNotExist(FilePath.DATA)

    def writeCSV(self, matchedList: List[str]) -> None:
        dataDict = {
            'Matched File': matchedList
        }
        df = pd.DataFrame(data=dataDict)
        filePath = FileHelper.joinPath(FilePath.DATA, TimeHelper.formatTime(fmt='%Y-%m-%d %H%M'))
        df.to_csv(f'{filePath}.csv')
