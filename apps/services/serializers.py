from django.db import transaction
from rest_framework import serializers
from apps.services.models import Service, ServiceOrder
from apps.client.models import Client, ClientComment
from apps.finance.models import Income, IncomeCategory

class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name_uz', 'name_ru', 'monthly_income']

class ServiceOrderCreateSerializer(serializers.Serializer):
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    price = serializers.IntegerField(required=False, allow_null=True)
    full_name = serializers.CharField()
    phone = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    service_id = serializers.UUIDField()

    def validate(self, data):
        try:
            service = Service.objects.get(id=data.get('service_id'))
        except Service.DoesNotExist:
            raise serializers.ValidationError("Service not found!")
        data['service'] = service
        return data

    def create(self, validated_data):
        with transaction.atomic():
            service_order = ServiceOrder.objects.create(
                date=validated_data.get('date'),
                start_time=validated_data.get('start_time'),
                end_time=validated_data.get('end_time'),
                price=validated_data.get('price'),
                full_name=validated_data.get('full_name'),
                phone=validated_data.get('phone'),
                description=validated_data.get('description'),
                service=validated_data.get('service'),
                type='crm'
            )
            client, _ = Client.objects.get_or_create(
                phone=service_order.phone,
                defaults={
                    'name': service_order.full_name,
                    'status': 'new'
                }
            )
            if service_order.description:
                ClientComment.objects.create(
                    client=client,
                    date=service_order.date,
                    comment=service_order.description
                )
            category, _ = IncomeCategory.objects.get_or_create(name='Mijozlar')
            if service_order.price is not None:
                Income.objects.create(
                    category=category,
                    price=service_order.price,
                    date=service_order.date,
                )
            return service_order

class ServiceOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = ['id', 'date', 'start_time', 'end_time', 'price', 'full_name', 'phone', 'description', 'type']