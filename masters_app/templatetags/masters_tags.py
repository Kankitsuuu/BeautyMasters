from django import template
from django.core.paginator import Paginator

from masters_app.models import *

# регистрация собственных шаблонных тегов
register = template.Library()

# simple tag
# @register.simple_tag()


@register.inclusion_tag('masters_app/link_footer.html', name='link_footer')
def get_link_footer(page):
    links = Link.objects.filter(page=page).select_related('link_type')
    return {'links': links}


@register.inclusion_tag('masters_app/pagination.html', name='pagination')
def html_paginator(page_obj):
    return {'page_obj': page_obj}
