from prompt_toolkit.validation import Validator, ValidationError


class HasInputValidator(Validator):
    def validate(self, document):
        if len(document.text) == 0:
            raise ValidationError(message='Please provide a valid input',
                                  cursor_position=len(document.text))
