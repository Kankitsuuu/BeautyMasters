from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .utils import DataMixin
from .forms import *

# Create your views here.


class HomeView(DataMixin, View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('User page')
        # else (user is not authenticated)
        context = HomeView.get_user_context(title='Beauty Masters', form=LoginUserForm)
        return render(request, 'masters_app/home.html', context=context)


def register(request):
    return HttpResponse('Страница для регистрации')


def master_page(request, master_slug):
    return HttpResponse('Личная страница пользователя')


def edit_master_page(request, master_slug):
    return HttpResponse('Настройки личной страницы пользователя')


def search_master(request):
    return HttpResponse('Страница для поиска мастера')
