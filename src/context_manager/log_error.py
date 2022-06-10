import sys
import traceback
from io import StringIO
from typing import List, Any

from src.constant.general import LoggingLevel
from src.context import messageHelper


class LogError:
    excludedExceptions: List[Any]
    noRaise: bool

    def __init__(self, excludedExceptions: List[Any] = None, noRaise: bool = False):
        self.noRaise = noRaise
        if excludedExceptions is not None:
            self.excludedExceptions = excludedExceptions
        else:
            self.excludedExceptions = []

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # lifted from https://gist.github.com/AlanCoding/288ee96b60e24c1f2cca47326e2c0af1
        # lifted from https://stackoverflow.com/questions/50233935/ignore-and-log-error-with-contextlib-contextmanager

        # We want the _full_ traceback with the context_manager
        # First we get the current call stack, which constitutes the "top",
        # it has the context_manager up to the point where the context_manager manager is used
        top_stack = StringIO()
        traceback.print_stack(file=top_stack)
        top_lines = top_stack.getvalue().strip('\n').split('\n')
        top_stack.close()
        # Get "bottom" stack from the local error that happened
        # inside the "with" block this wraps
        exc_type, exc_value, exc_traceback = sys.exc_info()

        # exclude exceptions
        for nException in self.excludedExceptions:
            if isinstance(exc_val, nException):
                return False

        if exc_type is None:
            return

        bottom_stack = StringIO()
        traceback.print_tb(exc_traceback, file=bottom_stack)
        bottom_lines = bottom_stack.getvalue().strip('\n').split('\n')
        # Glue together top and bottom where overlap is found
        bottom_cutoff = 0
        for i, line in enumerate(bottom_lines):
            if line in top_lines:
                # start of overlapping section, take overlap from bottom
                top_lines = top_lines[:top_lines.index(line)]
                bottom_cutoff = i
                break
        bottom_lines = bottom_lines[bottom_cutoff:]
        tb_lines = top_lines + bottom_lines

        tb_string = '\n'.join(
            ['Traceback (most recent call last):'] +
            tb_lines +
            ['{}: {}'.format(exc_type.__name__, str(exc_value))]
        )
        bottom_stack.close()
        # Log the combined stack

        messageHelper.log(tb_string, level=LoggingLevel.ERROR)
        if self.noRaise:
            return True
        return False
