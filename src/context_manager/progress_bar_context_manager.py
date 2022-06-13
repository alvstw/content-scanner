from threading import Event
from typing import Any

from tqdm import tqdm

from src import context
from src.context import threadManager
from src.utility.lock import Lock


class ProgressBarContextManager:
    _lock: Lock
    _tqdmInstance: tqdm

    _count: int

    counterExitEvent: Event

    def __init__(self, *args, **kwargs):
        self._lock = Lock()
        self._tqdmInstance = tqdm(*args, **kwargs)
        context.messageHelper.setProgressInstance(self._tqdmInstance)

        self._count = 0

        self.counterExitEvent = threadManager.ping(lambda: self.refresh())

    def __enter__(self):
        return self

    def setDescription(self, description: str, refresh: bool = True) -> None:
        self._tqdmInstance.set_description(description, refresh)

    def setPostfix(self, message='', refresh: bool = True) -> None:
        self._tqdmInstance.set_postfix_str(message, refresh)

    def update(self, n: Any = 1) -> None:
        if isinstance(n, int) > 0:
            self._count += n
        with self._lock.getLock():
            self._tqdmInstance.update(n)

    def refresh(self) -> None:
        self._tqdmInstance.refresh()

    def getCount(self) -> int:
        return self._count

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.counterExitEvent.set()
        context.messageHelper.clearProgressInstance()
        self._tqdmInstance.close()
