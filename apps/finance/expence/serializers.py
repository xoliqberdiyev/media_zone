from django.db import transaction
from rest_framework import serializers
from apps.finance.models import Expence, ExpenceCategory
from datetime import datetime
from django.db.models import Sum

class ExpenceCategorySerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ExpenceCategory
        fields = ['id', 'name', 'total_price']

    def get_total_price(self, obj):
        request = self.context.get('request')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        queryset = Expence.objects.filter(category=obj)
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__range=[start_date, end_date])
            except ValueError:
                pass

        return queryset.aggregate(total=Sum('price'))['total'] or 0

class ExpenceCreateSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    price = serializers.IntegerField()
    date = serializers.DateField()
    comment = serializers.CharField(required=False)

    def validate(self, data):
        try:
            category = ExpenceCategory.objects.get(id=data.get('category_id'))
        except ExpenceCategory.DoesNotExist:
            raise serializers.ValidationError("category not found")
        data['category'] = category
        return data

    def create(self, validated_data):
        with transaction.atomic():
            expence = Expence.objects.create(**validated_data)
            return expence

class ExpenceListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Expence
        fields = ['id', 'category', 'price', 'date', 'comment', 'created_at']

class ExpenceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expence
        fields = ['price', 'date', 'comment']

class ExpenceStatisticsSerializer(serializers.Serializer):
    total_expence = serializers.IntegerField()