import re
from typing import Any


class ValidateHelper:
    @staticmethod
    def isEmpty(value: Any) -> bool:
        from src.library.helper.data_helper import DataHelper
        value = DataHelper.convertToString(value)
        if len(value) != 0:
            return False
        return True

    @staticmethod
    def notEmpty(value: Any) -> bool:
        return not ValidateHelper.isEmpty(value)

    @staticmethod
    def isString(value: Any) -> bool:
        # noinspection PyBroadException
        try:
            str(value)
            return True
        except Exception:
            return False

    @staticmethod
    def isInteger(value: Any) -> bool:
        if isinstance(value, int):
            return True
        return False

    @staticmethod
    def isPositiveInteger(value: Any) -> bool:
        if ValidateHelper.isInteger(value):
            if value >= 0:
                return True
        return False

    @staticmethod
    def isValidRegex(value: str) -> bool:
        try:
            re.compile(value)
            return True
        except re.error:
            return False

