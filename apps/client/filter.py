import django_filters

from apps.client import models


class ClientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')
    phone = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = models.Client
        fields = ['name', 'phone']