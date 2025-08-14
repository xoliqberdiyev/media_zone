from django.db import transaction
from rest_framework import serializers
from apps.finance.models import Expence, ExpenceCategory

class ExpenceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenceCategory
        fields = ['id', 'name', 'total_price']

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
        return None

class ExpenceListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Expence
        fields = ['id', 'category', 'price', 'date', 'comment', 'created_at']

class ExpenceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expence
        fields = ['price', 'date', 'comment']