# apps/client/filter.py
import django_filters
from apps.client import models
from django.db.models import Q

class ClientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')
    phone = django_filters.CharFilter(method='filter_by_phone')
    comment = django_filters.CharFilter(method='filter_by_comment')

    class Meta:
        model = models.Client
        fields = ['name', 'phone', 'comment']

    def filter_by_phone(self, queryset, name, value):
        # Agar foydalanuvchi faqat 4 ta raqam kiritsa — endswith ishlatamiz
        if value.isdigit() and len(value) == 4:
            return queryset.filter(phone__endswith=value)
        # Aks holda to'liq yoki qisman kiritilgan raqamni qidiramiz
        return queryset.filter(phone__icontains=value)

    def filter_by_comment(self, queryset, name, value):
        return queryset.filter(comments__comment__icontains=value).distinct()
