import logging
from typing import List

from tqdm import tqdm

from src.constant.general import FilePath, LoggingLevel
from src.library.helper.console_helper import ConsoleHelper
from src.library.helper.file_helper import FileHelper
from src.library.helper.helper import Helper
from src.library.helper.string_helper import StringHelper


class MessageHelper:
    appName: str = 'Content Scanner'
    version: str

    symbol = ''
    desc = ''
    lineCount = 0
    messages: List[str] = []

    mainLogger: logging.Logger
    logger: logging.Logger

    _progressInstance: [tqdm, None] = None

    def __init__(self) -> None:
        self.version = Helper.getProjectMeta()['version']

        level = logging.INFO
        FileHelper.createDirectoryIfNotExist(FilePath.LOG)
        logfile = FileHelper.joinPath(FilePath.LOG, 'latest.log')

        formatter = logging.Formatter('[%(levelname)-5s] [%(asctime)s] %(message)s')
        handler = logging.FileHandler(logfile)
        handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.setLevel(level)
        logger.addHandler(handler)

        self.logger = logger

        logger.info('-' * 20 + f' {self.appName} ' + '-' * 20)
        logger.info(f'Version: {self.version}')

        logger.propagate = False

    def setProgressInstance(self, instance: tqdm) -> None:
        self._progressInstance = instance

    def getProgressInstance(self) -> [tqdm, None]:
        if self._progressInstance is not None:
            return self._progressInstance
        return None

    def clearProgressInstance(self) -> None:
        self._progressInstance = None

    def print(self, message: str = '', level: str = LoggingLevel.INFO, module: str = '', log: bool = True) -> None:
        progressInstance: [tqdm, None] = self.getProgressInstance()
        if progressInstance is None:
            ConsoleHelper.print(message)
        else:
            progressInstance.write(f'- {message}')
        if log:
            self.log(message=message, level=level, module=module)

    def log(self, message: str, level: str = LoggingLevel.INFO, module: str = '') -> None:
        logger = self.logger

        message = StringHelper.filterString(message)

        formattedModule = ''
        if module != '':
            formattedModule = f'<{module}> '

        if level == LoggingLevel.INFO:
            logger.info(f'{formattedModule}{message}')
        elif level == LoggingLevel.DEBUG:
            logger.debug(f'{formattedModule}{message}')
        elif level == LoggingLevel.ERROR:
            logger.error(f'{formattedModule}{message}')
