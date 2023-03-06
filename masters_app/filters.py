from django_filters.widgets import LinkWidget

from .models import Page, Category, City
import django_filters


class MastersFilter(django_filters.FilterSet):
    firstname = django_filters.CharFilter(lookup_expr='icontains', label="Ім'я")
    lastname = django_filters.CharFilter(lookup_expr='icontains', label="Прізвище")
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(),
                                                empty_label='Діяльність не обрано',
                                                label="Діяльність")
    city = django_filters.ModelChoiceFilter(queryset=City.objects.all(),
                                            empty_label='Місто не обрано',
                                            label="Місто")

    class Meta:

        model = Page
        fields = ['firstname', 'lastname', 'category', 'city']
