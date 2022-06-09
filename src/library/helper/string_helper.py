import re


class StringHelper:
    @staticmethod
    def filterString(testString: str, rule: str = r'[^A-Za-z\d_@.\\\/#&+-]+') -> str:
        return re.sub(rule, '', testString)
