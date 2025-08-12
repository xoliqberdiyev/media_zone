# apps/client/filter.py
import django_filters
from apps.client import models

class ClientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')
    phone = django_filters.CharFilter(lookup_expr='istartswith')
    comment = django_filters.CharFilter(method='filter_by_comment')

    class Meta:
        model = models.Client
        fields = ['name', 'phone', 'comment']

    def filter_by_comment(self, queryset, name, value):
        # comments__comment ichida izlash
        return queryset.filter(comments__comment__icontains=value).distinct()
