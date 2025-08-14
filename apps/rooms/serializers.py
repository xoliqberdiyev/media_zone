from django.db import transaction
from rest_framework import serializers
from apps.rooms.models import Room, RoomOrder
from apps.client.models import Client, ClientComment
from apps.finance.models import Income, IncomeCategory

class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name_uz', 'name_ru', 'monthly_income']

class RoomOrderCreateSerializer(serializers.Serializer):
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    price = serializers.IntegerField(required=False, allow_null=True)
    full_name = serializers.CharField()
    phone = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    room_id = serializers.UUIDField()
    servis_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)  # Optional field

    def validate(self, data):
        try:
            room = Room.objects.get(id=data.get('room_id'))
        except Room.DoesNotExist:
            raise serializers.ValidationError("Room not found!")
        data['room'] = room
        return data

    def create(self, validated_data):
        with transaction.atomic():
            # Create RoomOrder
            room_order = RoomOrder.objects.create(
                date=validated_data.get('date'),
                start_time=validated_data.get('start_time'),
                end_time=validated_data.get('end_time'),
                price=validated_data.get('price'),
                full_name=validated_data.get('full_name'),
                phone=validated_data.get('phone'),
                description=validated_data.get('description'),
                room=validated_data.get('room'),
                type='crm',
                servis_type=validated_data.get('servis_type')
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
                    date=room_order.date,
                    comment=validated_data.get('description')
                )
            # Create Income if price exists
            if validated_data.get('price') is not None:
                category, _ = IncomeCategory.objects.get_or_create(name='Mijozlar')
                Income.objects.create(
                    category=category,
                    price=validated_data.get('price'),
                    date=room_order.date,
                )
            return room_order

class RoomOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomOrder
        fields = ['id', 'date', 'start_time', 'end_time', 'price', 'full_name', 'phone', 'description', 'type', 'servis_type']  # Included servis_type

class RoomOrderUpdateSerializer(serializers.ModelSerializer):
    date = serializers.DateField(required=False)
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)
    price = serializers.IntegerField(required=False, allow_null=True)
    full_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    room_id = serializers.UUIDField(required=False)
    servis_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)  # Optional field

    class Meta:
        model = RoomOrder
        fields = ['date', 'start_time', 'end_time', 'price', 'full_name', 'phone', 'description', 'room_id', 'servis_type']  # Included servis_type

    def validate(self, data):
        if 'room_id' in data:
            try:
                room = Room.objects.get(id=data.get('room_id'))
                data['room'] = room
            except Room.DoesNotExist:
                raise serializers.ValidationError("Room not found!")
        return data

    def update(self, instance, validated_data):
        with transaction.atomic():
            room = validated_data.pop('room', None)
            if room:
                instance.room = room
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