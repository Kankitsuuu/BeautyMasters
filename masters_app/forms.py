from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логін'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Ім'я"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Прізвище'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повторіть пароль'}))


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логін'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))


class ChangePageForm(forms.ModelForm):
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
            'firstname': forms.TextInput(attrs={'class': 'form-control bg-transparent text-light fs-2'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control bg-transparent text-light fs-2'}),
            'about': forms.Textarea(attrs={'cols': 100, 'rows': 15}),

        }


class EditAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control bg-transparent'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-transparent'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-transparent'}),
            'email': forms.TextInput(attrs={'class': 'form-control bg-transparent'}),
        }


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
        labels = {'name': 'Назва альбома',
                  'main_picture': 'Головне фото'}
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Опис альбома', })
        }

