import threading
from typing import Union

from src.constant.general import LockType


class Lock:
    lock: Union[threading.Lock, threading.Semaphore]

    def __init__(self, lockType: str = LockType.LOCK, semaphoreCount: int = 1):
        if lockType == LockType.LOCK:
            self.lock = threading.Lock()
        elif lockType == LockType.SEMAPHORE:
            self.lock = threading.Semaphore(semaphoreCount)

    def acquire(self, blocking: bool = True) -> bool:
        return self.lock.acquire(blocking=blocking)

    def release(self) -> None:
        self.lock.release()

    def getLock(self) -> Union[threading.Lock, threading.Semaphore]:
        return self.lock

    def isLocked(self) -> bool:
        return self.lock.locked()
