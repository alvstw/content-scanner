import re


class StringHelper:
    @staticmethod
    def filterString(testString: str, rule: str = r'/^[ A-Za-z0-9_@./#&+-]*$/') -> str:
        return re.sub(rule, '', testString)
