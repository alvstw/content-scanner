import threading

from scanner.src.constant.general import LockType
from scanner.src.message_helper import MessageHelper
from scanner.src.thread_manager import ThreadManager
from scanner.src.utility.lock import Lock

discoveryPhaseThreadCount = 25
readingPhaseThreadCount = 25

messageHelper = MessageHelper()
threadManager = ThreadManager(messageHelper)
discoveryPhaseIdleLock = Lock(LockType.SEMAPHORE, discoveryPhaseThreadCount - 1)
discoveryPhaseExitEvent = threading.Event()
