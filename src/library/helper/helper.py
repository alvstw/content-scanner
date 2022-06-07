import os
import shutil as sh
from collections import defaultdict
from datetime import date, datetime
from json import JSONEncoder

import tomlkit as tomlkit


class Helper:
    @staticmethod
    def getProjectMeta():
        with open('./pyproject.toml') as pyproject:
            file_contents = pyproject.read()

        return tomlkit.parse(file_contents)['tool']['poetry']

    @staticmethod
    def nestedDict(n, datatype):
        if n == 1:
            return defaultdict(datatype)
        else:
            return defaultdict(lambda: Helper.nestedDict(n - 1, datatype))

    @staticmethod
    def getTerminalWidth():
        return sh.get_terminal_size().columns

    @staticmethod
    def lookahead(iterable):
        """Pass through all values from the given iterable, augmented by the
        information if there are more values to come after the current one
        (True), or if it is the last value (False).
        """
        # Get an iterator and pull the first value.
        it = iter(iterable)
        last = next(it)
        # Run the iterator to exhaustion (starting from the second value).
        for val in it:
            # Report the *previous* value (more to come).
            yield last, True
            last = val
        # Report the last value.
        yield last, False

    @staticmethod
    def stringToBoolean(value) -> [bool, None]:
        if not isinstance(value, str):
            return None
        if value.lower() == 'true':
            return True
        if value.lower() == 'false':
            return False
        return None


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
