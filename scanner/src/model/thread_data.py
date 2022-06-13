import threading
from datetime import datetime

from scanner.src.library.helper.time_helper import TimeHelper


class ThreadData:
    thread: threading.Thread
    threadType: str
    createdAt: datetime

    def __init__(self, thread: threading.Thread, threadType: str, threadCounter: int = None) -> None:
        self.thread = thread
        self.threadType = threadType
        self.threadCounter = threadCounter
        self.createdAt = TimeHelper.getUTCTime()
