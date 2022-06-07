from typing import Any


class DataHelper:
    @staticmethod
    def convertToInteger(value: Any) -> [int, None]:
        try:
            return int(value)
        except ValueError:
            return None

    @staticmethod
    def convertToString(value: Any) -> [str, None]:
        from src.library.helper.validate_helper import ValidateHelper
        if ValidateHelper.isString(value):
            return str(value)
        return None
