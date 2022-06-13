from os import path

from prompt_toolkit.validation import Validator, ValidationError


class PathValidator(Validator):
    def validate(self, document):
        if not path.exists(document.text):
            raise ValidationError(message='The path does not exist',
                                  cursor_position=len(document.text))
        if not path.isdir(document.text):
            raise ValidationError(message='The path is not a directory',
                                  cursor_position=len(document.text))
