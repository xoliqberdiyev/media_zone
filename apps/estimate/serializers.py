from django.db import transaction

from rest_framework import serializers

from .models import Estimate


class EstimateIncomeCreateSerializer(serializers.Serializer):
    reason = serializers.CharField()
    date = serializers.DateField()
    description = serializers.CharField()
    price = serializers.IntegerField()

    def create(self, validated_data):
        with transaction.atomic():
            estimate = Estimate.objects.create(
                type='INCOME',
                reason=validated_data.get('reason'),
                date=validated_data.get('date'),
                description=validated_data.get('description'),
                price=validated_data.get('price')
            )
            return estimate
        
    

class EstimateExpenceCreateSerializer(serializers.Serializer):
    reason = serializers.CharField()
    date = serializers.DateField()
    description = serializers.CharField()
    price = serializers.IntegerField()

    def create(self, validated_data):
        with transaction.atomic():
            estimate = Estimate.objects.create(
                type='EXPENCE',
                reason=validated_data.get('reason'),
                date=validated_data.get('date'),
                description=validated_data.get('description'),
                price=validated_data.get('price')
            )
            return estimate
        

class EstimateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = [
            'id', 'reason', 'date', 'description', 'type', 'price'
        ]