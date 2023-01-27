from .models import *

menu = [{'title': "Додому", 'url_name': 'home'},
        {'title': "Зворотній зв'язок", 'url_name': 'home'},

]


class DataMixin:
    @staticmethod
    def get_user_context(**kwargs):
        context = kwargs
        context['menu'] = menu
        return context