from django.db import transaction
from rest_framework import serializers
from apps.finance.models import Income, IncomeCategory
from django.db.models import Sum

class IncomeCategorySerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = IncomeCategory
        fields = ['id', 'name', 'total_price']

    def get_total_price(self, obj):
        # Faqat berilgan tranzaksiyalarni hisoblash uchun context ishlatiladi
        queryset = self.context.get('queryset', Income.objects.filter(category=obj))
        total = queryset.aggregate(total_price=Sum('price'))['total_price'] or 0
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

class IncomeListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Income
        fields = ['id', 'category', 'price', 'date', 'comment', 'created_at']

class IncomeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['price', 'date', 'comment']

class IncomeStatisticsSerializer(serializers.Serializer):
    total_income = serializers.IntegerField()