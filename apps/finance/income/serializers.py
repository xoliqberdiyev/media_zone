from django.db import transaction
from rest_framework import serializers
from apps.finance.models import Income, IncomeCategory
from datetime import datetime
from django.db.models import Sum
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class IncomeCategorySerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = IncomeCategory
        fields = ['id', 'name', 'total_price']

    def get_total_price(self, obj):
        request = self.context.get('request')
        view = self.context.get('view')
        queryset = Income.objects.filter(category=obj)

        if view and hasattr(view, 'paginator') and request:
            paginator = view.paginator
            try:
                paginated_queryset = paginator.paginate_queryset(queryset, request, view=view)
                logger.debug(f"Joriy sahifa yozuvlari soni: {len(paginated_queryset)}")
                logger.debug(f"Joriy sahifa yozuvlari: {[item.price for item in paginated_queryset]}")
                total = sum(item.price for item in paginated_queryset) if paginated_queryset else 0
            except Exception as e:
                logger.error(f"Pagination xatosi: {e}")
                total = queryset.aggregate(total=Sum('price'))['total'] or 0
        else:
            total = queryset.aggregate(total=Sum('price'))['total'] or 0

        logger.debug(f"Hisoblangan total_price '{obj.name}' uchun: {total}")
        return total

class IncomeCreateSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    price = serializers.IntegerField()
    date = serializers.DateField()
    comment = serializers.CharField(required=False)

    def validate(self, data):
        try:
            category = IncomeCategory.objects.get(id=data.get('category_id'))
        except IncomeCategory.DoesNotExist:
            raise serializers.ValidationError("category not found")
        data['category'] = category
        return data

    def create(self, validated_data):
        with transaction.atomic():
            income = Income.objects.create(**validated_data)
            return income
        return None

class IncomeListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Income
        fields = ['id', 'category', 'price', 'date', 'comment', 'created_at', 'total_price']

    def get_total_price(self, obj):
        request = self.context.get('request')
        view = self.context['view']
        queryset = view.get_queryset()

        paginator = view.paginator
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=view)

        total = sum(item.price for item in paginated_queryset) if paginated_queryset else 0
        return total

class IncomeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['price', 'date', 'comment']

class IncomeStatisticsSerializer(serializers.Serializer):
    total_income = serializers.IntegerField()