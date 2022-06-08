import typer
from PyInquirer import prompt

from src.constant.fileType import FileType
from src.library.helper.data_helper import DataHelper
from src.library.helper.validate_helper import ValidateHelper
from src.report_service import ReportService
from src.search_service import SearchService
from src.validator.console.path_validator import PathValidator
from src.validator.console.positive_number_validator import PositiveNumberValidator


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
            'name': 'scanTypes',
            'message': 'Files Type',
            'choices': [
                {
                    'name': FileType.rpaFile,
                    'checked': True
                },
                {
                    'name': FileType.excelFile,
                    'disabled': 'Currently not supported'
                },
                {
                    'name': FileType.otherFIle,
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

    searchService: SearchService = SearchService()
    reportService: ReportService = ReportService()

    scanDirectory: str = answers['scanDirectory']
    # TODO: read scan types from user input
    # scanTypes: List[str] = answers['scanTypes']
    scanKeyword: str = answers['scanKeyword']
    caseSensitive: bool = answers['caseSensitive']
    scanDepth: [int, None] = answers['scanDepth'] if answers['scanDepth'] != 0 else None

    rs = searchService.searchKeyword(scanDirectory, scanKeyword, depth=scanDepth, caseSensitive=caseSensitive)
    reportService.writeCSV(rs)


if __name__ == "__main__":
    # launch main program
    typer.run(main)
