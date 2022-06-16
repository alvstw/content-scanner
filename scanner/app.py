import sys
from typing import List

import typer
from PyInquirer import prompt

from scanner.src.constant.fileType import RpaFileType, ExcelFileType, AllFileType, OtherFileType
from scanner.src.context import threadManager, messageHelper
from scanner.src.library.helper.data_helper import DataHelper
from scanner.src.library.helper.file_helper import FileHelper
from scanner.src.library.helper.validate_helper import ValidateHelper
from scanner.src.report_service import ReportService
from scanner.src.search_service import SearchService
from scanner.src.validator.console.path_validator import PathValidator
from scanner.src.validator.console.positive_number_validator import PositiveNumberValidator


def main():
    questions = [
        {
            'type': 'input',
            'name': 'scanDirectory',
            'message': 'Scan Directory',
            'validate': PathValidator
        },
        {
            'type': 'checkbox',
            'name': 'scanFileTypes',
            'message': 'Files Type',
            'choices': [
                {
                    'name': AllFileType.name,
                    'checked': True
                },
                {
                    'name': RpaFileType.name,
                },
                {
                    'name': ExcelFileType.name,
                    'disabled': 'Currently not supported'
                },
                {
                    'name': OtherFileType.name,
                }
            ],
        },
        {
            'type': 'input',
            'name': 'scanKeyword',
            'message': 'Scan Keyword',
            'validate': ValidateHelper.notEmpty
        },
        {
            'type': 'input',
            'name': 'exclusionRule',
            'message': 'Exclusion Rule',
            'validate': lambda value: value == '' or ValidateHelper.isValidRegex(value)
        },
        {
            'type': 'confirm',
            'name': 'caseSensitive',
            'message': 'Case Sensitive',
            'default': False
        },
        {
            'type': 'input',
            'name': 'scanDepth',
            'message': 'Scan Level (0 = search every depth)',
            'default': '0',
            'validate': PositiveNumberValidator,
            'filter': DataHelper.convertToInteger
        },

    ]

    answers = prompt(questions)

    if len(answers) == 0:
        threadManager.setExit()
        sys.exit(1)

    searchService: SearchService = SearchService()
    reportService: ReportService = ReportService()

    debug = False

    scanDirectory: str = answers['scanDirectory']
    scanFileTypes: List[str] = answers['scanFileTypes']
    scanKeyword: str = answers['scanKeyword']
    exclusionRule: str = answers['exclusionRule'] if answers['exclusionRule'] != '' else None
    caseSensitive: bool = answers['caseSensitive']
    scanDepth: [int, None] = answers['scanDepth'] if answers['scanDepth'] != 0 else None

    rs = searchService.searchKeyword(scanDirectory, scanKeyword, scanFileTypes=scanFileTypes,
                                     exclusionRule=exclusionRule, depth=scanDepth, caseSensitive=caseSensitive)
    csvName = reportService.writeCSV(rs)

    messageHelper.print(f'Saved result to: {csvName}')

    if debug:
        messageHelper.print(f'Debug Info:')
        messageHelper.print(f'FileHelper.isFile: {FileHelper.isFile.cache_info()}')
        messageHelper.print(f'FileHelper.isDirectory: {FileHelper.isDirectory.cache_info()}')
        messageHelper.print(f'FileHelper.listDirectory: {FileHelper.listDirectory.cache_info()}')

    threadManager.setExit()


if __name__ == "__main__":
    # launch main program
    typer.run(main)
