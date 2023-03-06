from django.core.paginator import Paginator
from .models import *

menu = [
        {'title': "Додому", 'url_name': 'home'},
        {'title': "Пошук майстрів", 'url_name': 'search'},
        ]


class DataMixin:
    @staticmethod
    def get_user_context(**kwargs):
        context = kwargs
        context['menu'] = menu
        return context

    @staticmethod
    def get_paginator(request, model, count, **kwargs):
        m = model.objects.filter(**kwargs)
        paginator = Paginator(m, count)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj

