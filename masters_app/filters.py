from .models import Page, Category, City
import django_filters


class MastersFilter(django_filters.FilterSet):
    firstname = django_filters.CharFilter(lookup_expr='icontains')
    lastname = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(),
                                              empty_label='Category not selected',
                                              )
    city = django_filters.ModelChoiceFilter(queryset=City.objects.all(),
                                              empty_label='City not selected',
                                              )

    class Meta:
        model = Page
        fields = ['firstname', 'lastname', 'category', 'city']