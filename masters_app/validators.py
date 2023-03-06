from django.contrib.auth.password_validation import CommonPasswordValidator
from django.core.exceptions import ValidationError


class CustomMinimumLengthPasswordValidator:

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                message=f'Пароль занадто короткий.Пароль повинен містити щонайменш {self.min_length} символів.',
                code="password_too_short",
                params={"min_length": self.min_length},
            )

    def get_help_text(self):
        message = f'Пароль повинен містити щонайменш {self.min_length} символів.'
        return message


class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
               message='Цей пароль занадто легкий.'
            )

    def get_help_text(self):
        return "Не використовуйте занадто легкі та найбільшвживані паролі."


class CustomNumericPasswordValidator:
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                message='Пароль не може складатися тільки з цифр',
                code="password_entirely_numeric",
            )

    def get_help_text(self):
        return "Пароль не може складатися тільки з цифр"