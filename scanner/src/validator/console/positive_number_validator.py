from prompt_toolkit.validation import ValidationError, Validator

from scanner.src.library.helper.data_helper import DataHelper
from scanner.src.library.helper.validate_helper import ValidateHelper


class PositiveNumberValidator(Validator):
    def validate(self, document):
        if ValidateHelper.isEmpty(document.text):
            raise ValidationError(message='Please enter a number')

        value = DataHelper.convertToInteger(document.text)
        if value is None:
            raise ValidationError(message='Please enter a number',
                                  cursor_position=len(document.text))

        if not ValidateHelper.isPositiveInteger(value):
            raise ValidationError(message='Please enter a positive number',
                                  cursor_position=len(document.text))
