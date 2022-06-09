import random
import threading
from time import sleep
from typing import List, Any, Callable

from src.constant.general import LockType
from src.message_helper import MessageHelper
from src.model.thread_data import ThreadData
from src.utility.lock import Lock


class ThreadType:
    THREAD = 'Thread'
    READ_FILE_THREAD = 'ReadFileThread'
    DISCOVERY_THREAD = 'DiscoveryThread'
    PING_THREAD = 'PingThread'


class ThreadManager:
    _messageHelper: MessageHelper

    _threadDataList: List[ThreadData]
    _threadCounters: dict[str, list] = {}

    _lock: Lock

    _exitEvent: threading.Event

    def __init__(self, messageHelper: MessageHelper, maxThread: int = 100) -> None:
        self._messageHelper = messageHelper
        self._threadDataList = []
        self._databaseThreads = []

        self._lock = Lock(LockType.SEMAPHORE, maxThread)
        self._exitEvent = threading.Event()

        threadWatcher = threading.Thread(target=self._threadWatcher, name='ThreadWatcher')
        threadWatcher.start()

    def add(self, thread: threading.Thread, name: Any = None, threadType: str = ThreadType.THREAD,
            blockingLock=True) -> threading.Thread:
        if isinstance(name, str):
            thread.setName(name)
            self._threadDataList.append(ThreadData(thread, ThreadType.THREAD))

        else:
            counter = self._addCounter(threadType)
            thread.setName(f'{threadType}-{counter}')
            self._threadDataList.append(ThreadData(thread, threadType, threadCounter=counter))

        self._messageHelper.log(f'New thread has been created: {thread.getName()}')

        if self._lock.acquire(blocking=blockingLock):
            thread.start()
        return thread

    def execute(self, target: Any, args: tuple = (), name: Any = None, threadType: str = ThreadType.THREAD,
                blockingLock=True) \
            -> threading.Thread:
        args = (target,) + args
        if isinstance(name, str):
            thread = threading.Thread(target=self._exec, args=args, name=f'{name}')
            return self.add(thread, name, blockingLock=blockingLock)

        elif threadType == ThreadType.THREAD:
            thread = threading.Thread(target=self._exec, args=args)
            return self.add(thread, threadType=threadType, blockingLock=blockingLock)
        else:
            thread = threading.Thread(target=self._exec, args=args, )
            return self.add(thread, threadType=threadType, blockingLock=blockingLock)

    def hasActiveThread(self, threadType: str = None) -> bool:
        if threadType is None:
            return len(self._threadDataList) > 0
        for thread in self._threadDataList:
            if thread.threadType == threadType:
                if thread.thread.is_alive():
                    return True
        return False

    def joinThreads(self, threadType: str, timeout: [int, None] = None) -> bool:
        while self.hasActiveThread(threadType):
            for thread in self._threadDataList:
                if thread.threadType == threadType:
                    thread.thread.join(timeout=timeout)
                    if thread.thread.is_alive():
                        pass
                        # TODO
        return False

    def setExit(self) -> None:
        self._exitEvent.set()

    def ping(
            self, call: Callable, exitEvent: threading.Event = threading.Event(), interval: float = 1, *args
    ) -> threading.Event:
        args = (call, exitEvent, interval,) + args
        self.execute(self._pinger, args=args, threadType=ThreadType.PING_THREAD)
        return exitEvent

    def _pinger(self, call: Callable, exitEvent: threading.Event, interval: float = 1, *args, **kwargs) -> None:
        while True:
            if exitEvent.is_set():
                return
            sleep(interval)
            call(*args, **kwargs)

    def _addCounter(self, threadType: str) -> int:
        counterList: List[int] = self._threadCounters.get(threadType, None)
        if counterList is None:
            counterList = []
        maxLength = 999
        if len(counterList) > 999:
            maxLength = len(counterList) + 100
        while True:

            counter = random.randint(1, maxLength)
            if counter not in counterList:
                counterList.append(counter)
                self._threadCounters[threadType] = counterList
                return counter

    def _removeCounter(self, threadType: str, counter: int) -> bool:
        counterList: List[int] = self._threadCounters.get(threadType, None)
        if counterList is None:
            return False
        if counter not in counterList:
            return False
        counterList.remove(counter)
        return True

    def _threadWatcher(self) -> None:
        while True:
            sleep(1)
            if self._exitEvent.is_set() and not self.hasActiveThread():
                return
            for thread in self._threadDataList:
                if not thread.thread.is_alive():
                    # Remove from helper's list
                    self._threadDataList.remove(thread)
                    threadName = thread.thread.getName()
                    # Adjust counter
                    if thread.threadType != ThreadType.THREAD or thread.threadCounter is not None:
                        self._removeCounter(thread.threadType, thread.threadCounter)
                    # Print message
                    self._messageHelper.log(f'{threadName} has been terminated')

    def _exec(self, target: Any, *args, **kwargs):
        target(*args, **kwargs)
        self._lock.getLock().release()
