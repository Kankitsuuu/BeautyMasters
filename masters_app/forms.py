from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логін'}),
                               validators=[UnicodeUsernameValidator(message='Юзернейм є не валідним. '
                                                                            'Ви можете літери, цифри та символи: @/./+/-/_. ')])
    first_name = forms.CharField(min_length=2, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Ім'я"}))
    last_name = forms.CharField(min_length=2, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Прізвище'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
                            validators=[EmailValidator(message='Email є невалідним.')])
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повторіть пароль'}))
    error_messages = {"password_mismatch": 'Введені паролі відрізняються',
                      "invalid_login": 'Введіть валідний юзернейм'}


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логін'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))
    error_messages = {
                      "invalid_login": "Ви ввели неправильний логін або пароль.",
                      "inactive": "Цей акаунт не є дійсним."
                     }


class ChangePageForm(forms.ModelForm):
    firstname = forms.CharField(min_length=2,
                                widget=forms.TextInput(attrs={'class': 'form-control bg-transparent text-light fs-2'}))
    lastname = forms.CharField(min_length=2,
                               widget=forms.TextInput(attrs={'class': 'form-control bg-transparent text-light fs-2'}))

    class Meta:
        model = Page
        fields = ('firstname', 'lastname', 'category', 'user_photo', 'background', 'city', 'about')
        labels = {'firstname': "Ім'я:",
                  'lastname': 'Прізвище:',
                  'about': 'Про мене:',
                  'category': 'Діяльність:',
                  'city': 'Місто:',
                  }
        widgets = {
            'about': forms.Textarea(attrs={'cols': 100, 'rows': 15}),

        }


class EditAccountForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control bg-transparent'}),
                               validators=[UnicodeUsernameValidator(message='Юзернейм є не валідним. '
                                                                            'Ви можете літери, цифри та символи: @/./+/-/_. ')])
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control bg-transparent'}),
                            validators=[EmailValidator(message='Email є невалідним.')])
    first_name = forms.CharField(min_length=2, widget=forms.TextInput(attrs={'class': 'form-control bg-transparent'}))
    last_name = forms.CharField(min_length=2, widget=forms.TextInput(attrs={'class': 'form-control bg-transparent'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class LinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['link_type'].empty_label = 'Тип посилання'

    class Meta:
        model = Link
        fields = ('link_type', 'url')


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('main_picture', 'name', 'description')
        labels = {
            'name': 'Назва альбома',
            'main_picture': 'Головне фото'
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Опис альбома', })
        }


class WorkForm(forms.ModelForm):

    class Meta:
        model = Work
        fields = ('photo', 'description')
        labels = {
            'photo': 'Фото',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Опис роботи', }),
        }


class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старий пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
    new_password1 = forms.CharField(
        label="Новий пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Повторіть пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )


