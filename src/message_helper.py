import logging
from typing import List

from src.constant.general import FilePath, LoggingLevel
from src.library.helper.console_helper import ConsoleHelper
from src.library.helper.helper import Helper


class MessageHelper:
    appName: str = 'Content Scanner'
    version: str

    symbol = ''
    desc = ''
    lineCount = 0
    messages: List[str] = []

    mainLogger: logging.Logger
    logger: logging.Logger

    def __init__(self) -> None:
        self.version = Helper.getProjectMeta()['version']

        level = logging.INFO
        logfile = f'{FilePath.LOG}/latest.log'

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

    def print(self, message: str = '', level: str = LoggingLevel.INFO, module: str = '', log: bool = True) -> None:
        ConsoleHelper.print(message)
        self.log(message=message, level=level, module=module)

    def log(self, message: str, level: str = LoggingLevel.INFO, module: str = '') -> None:
        logger = self.logger

        formattedModule = ''
        if module != '':
            formattedModule = f'<{module}> '

        if level == LoggingLevel.INFO:
            logger.info(f'{formattedModule}{message}')
        elif level == LoggingLevel.DEBUG:
            logger.debug(f'{formattedModule}{message}')
        elif level == LoggingLevel.ERROR:
            logger.error(f'{formattedModule}{message}')
