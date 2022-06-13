import logging

from tqdm import tqdm

from scanner.src.constant.general import FilePath, LoggingLevel
from scanner.src.library.helper.console_helper import ConsoleHelper
from scanner.src.library.helper.file_helper import FileHelper
from scanner.src.library.helper.helper import Helper
from scanner.src.library.helper.string_helper import StringHelper
from scanner.src.utility.lock import Lock


class MessageHelper:
    _appName: str = 'Content Scanner'
    _version: str

    _logger: logging.Logger

    _lock: Lock
    _progressInstance: [tqdm, None] = None

    def __init__(self) -> None:
        self._version = Helper.getProjectMeta()['version']

        self._lock = Lock()

        level = logging.INFO
        FileHelper.createDirectoryIfNotExist(FilePath.LOG)
        logfile = FileHelper.joinPath(FilePath.LOG, 'latest.log')

        # noinspection SpellCheckingInspection
        formatter = logging.Formatter('[%(threadName)-20s:%(levelname)-5s] [%(asctime)s] %(message)s')
        handler = logging.FileHandler(logfile)
        handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.setLevel(level)
        logger.addHandler(handler)

        self._logger = logger

        logger.info('-' * 20 + f' {self._appName} ' + '-' * 20)
        logger.info(f'Version: {self._version}')

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
        with self._lock.getLock():
            progressInstance: [tqdm, None] = self.getProgressInstance()
            if progressInstance is None:
                ConsoleHelper.print(message)
            else:
                formattedMessage, _ = ConsoleHelper.formatWithIndent(message)
                progressInstance.write(formattedMessage)
            if log:
                self.log(message=message, level=level, module=module)

    def log(self, message: str, level: str = LoggingLevel.INFO, module: str = '') -> None:
        logger = self._logger

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
