import sys
import textwrap as tr

from src.library.helper.helper import Helper


class ConsoleHelper:
    @staticmethod
    def deleteLines(count: int = 1) -> None:
        for i in range(count):
            sys.stdout.write('\x1b[1A')  # cursor up
            sys.stdout.write('\x1b[2K')  # erase line

    @staticmethod
    def printFullLine(character: str = '-') -> None:
        line = character * Helper.getTerminalWidth()
        print(line)

    @staticmethod
    def printHalfLine(character: str = '-') -> None:
        line = character * int(Helper.getTerminalWidth() / 2)
        print(line)

    @staticmethod
    def print(message: str = '', prefix: str = '- ') -> int:
        if not isinstance(message, str):
            message = str(message)
        if message == '':
            print()
            return 1

        rs, lineCount = ConsoleHelper.formatWithIndent(message, prefix)
        print(rs)
        return lineCount

    @staticmethod
    def formatWithIndent(message: str, prefix: str = '- ') -> (str, int):
        rs = ''
        indentSpace = ' ' * len(prefix)
        bodyLineWidth = Helper.getTerminalWidth() - len(prefix)
        content = message.split('\n')
        isFirstLine = True
        lineCount = 0
        for c, cHasMore in Helper.lookahead(content):
            lines = tr.wrap(c, width=bodyLineWidth)
            for line, lHasMore in Helper.lookahead(lines):
                if isFirstLine:
                    rs += f'{prefix}{line}'
                    isFirstLine = False
                    rs += '\n' if lHasMore else ''
                    lineCount += 1
                    continue
                rs += f'{indentSpace}{line}'
                rs += '\n' if cHasMore else ''
                lineCount += 1
        return rs, lineCount

    @staticmethod
    def input(desc=''):
        i = input(f'{desc} >> ')
        return i
