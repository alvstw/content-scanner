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

        indentSpace = ' ' * len(prefix)
        bodyLineWidth = Helper.getTerminalWidth() - 4
        content = message.split('\n')
        isFirstLine = True
        lineCount = 0
        for c in content:
            lines = tr.wrap(c, width=bodyLineWidth)
            for line in lines:
                if isFirstLine:
                    print(f'{prefix}{line}')
                    isFirstLine = False
                    lineCount += 1
                    continue
                print(f'{indentSpace}{line}')
                lineCount += 1
        return lineCount

    @staticmethod
    def input(desc=''):
        i = input(f'{desc} >> ')
        return i
