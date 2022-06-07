from time import sleep
from typing import List

import typer
from PyInquirer import prompt
from tqdm import tqdm

from src.constant.fileType import FileType
from src.library.helper.data_helper import DataHelper
from src.library.helper.validate_helper import ValidateHelper
from src.validator.console.path_validator import PathValidator
from src.validator.console.positive_number_validator import PositiveNumberValidator
from src.message_helper import MessageHelper


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
                    'name': FileType.excelFile
                },
                {
                    'name': FileType.otherFIle
                }
            ],
        },
        {
            'type': 'input',
            'name': 'scanKeyword',
            'message': 'Scan Keyword',
            'validate': ValidateHelper.isEmpty
        },
        {
            'type': 'confirm',
            'name': 'caseSensitive',
            'message': 'Case Sensitive',
            'default': False
        },
        {
            'type': 'input',
            'name': 'scanLevel',
            'message': 'Scan Level (0 = search every level)',
            'default': '0',
            'validate': PositiveNumberValidator,
            'filter': DataHelper.convertToInteger
        },

    ]

    answers = prompt(questions)

    scanDirectory: str = answers['scanDirectory']
    scanTypes: List[str] = answers['scanTypes']
    scanKeyword: str = answers['scanKeyword']
    caseSensitive: bool = answers['caseSensitive']
    scanLevel: int = answers['scanLevel']

    with tqdm(total=100) as pbar:
        for i in range(100):
            sleep(0.1)
            pbar.update(1)


if __name__ == "__main__":
    # init
    messageHelper = MessageHelper()

    # launch main program
    typer.run(main)
