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
            # Create ServiceOrder
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
            # Create or get Client
            client, created = Client.objects.get_or_create(
                phone=validated_data.get('phone'),
                defaults={
                    'name': validated_data.get('full_name'),
                    'status': 'new'
                }
            )
            if not created:
                # Update name if client already exists
                client.name = validated_data.get('full_name')
                client.save()
            # Create ClientComment if description exists
            if validated_data.get('description'):
                ClientComment.objects.create(
                    client=client,
                    date=service_order.date,
                    comment=validated_data.get('description')
                )
            # Create Income if price exists
            if validated_data.get('price') is not None:
                category, _ = IncomeCategory.objects.get_or_create(name='Mijozlar')
                Income.objects.create(
                    category=category,
                    price=validated_data.get('price'),
                    date=service_order.date,
                )
            return service_order

class ServiceOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = ['id', 'date', 'start_time', 'end_time', 'price', 'full_name', 'phone', 'description', 'type']

class ServiceOrderUpdateSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=False)
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)
    price = serializers.IntegerField(required=False, allow_null=True)
    full_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    service_id = serializers.UUIDField(required=False)

    class Meta:
        model = ServiceOrder
        fields = ['date', 'start_time', 'end_time', 'price', 'full_name', 'phone', 'description', 'service_id']

    def validate(self, data):
        if 'service_id' in data:
            try:
                service = Service.objects.get(id=data.get('service_id'))
                data['service'] = service
            except Service.DoesNotExist:
                raise serializers.ValidationError("Service not found!")
        return data

    def update(self, instance, validated_data):
        with transaction.atomic():
            service = validated_data.pop('service', None)
            if service:
                instance.service = service
            if 'description' in validated_data and validated_data['description']:
                client, _ = Client.objects.get_or_create(
                    phone=validated_data.get('phone', instance.phone),
                    defaults={
                        'name': validated_data.get('full_name', instance.full_name),
                        'status': 'new'
                    }
                )
                ClientComment.objects.create(
                    client=client,
                    date=validated_data.get('date', instance.date),
                    comment=validated_data['description']
                )
            if 'price' in validated_data and validated_data['price'] is not None:
                category, _ = IncomeCategory.objects.get_or_create(name='Mijozlar')
                Income.objects.create(
                    category=category,
                    price=validated_data['price'],
                    date=validated_data.get('date', instance.date),
                )
            return super().update(instance, validated_data)