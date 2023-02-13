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
        fields = ['firstname', 'lastname', 'category', 'city', 'about']
        labels = {'firstname': "Ім'я:",
                  'lastname': 'Прізвище:',
                  'about': 'Про мене:',
                  'category': 'Категорія',
                  'city': 'Місто',
                  }
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control bg-transparent text-light fs-1'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control bg-transparent text-light fs-1'}),
            'about': forms.Textarea(attrs={'cols': 50, 'rows': 10}),

        }
