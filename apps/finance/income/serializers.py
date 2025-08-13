from datetime import datetime

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
        request = self.context.get('request')
        category_id = obj.id
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        queryset = Income.objects.filter(category__id=category_id)
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__range=[start_date, end_date])
            except ValueError:
                pass

        return queryset.aggregate(total=Sum('price'))['total'] or 0

        queryset = Income.objects.filter(category=obj)
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__range=[start_date, end_date])
            except ValueError:
                pass

        return queryset.aggregate(total=Sum('price'))['total'] or 0

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

    class Meta:
        model = Income
        fields = ['id', 'category', 'price', 'date', 'comment', 'created_at']

class IncomeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['price', 'date', 'comment']

class IncomeStatisticsSerializer(serializers.Serializer):
    total_income = serializers.IntegerField()
