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
    price = serializers.IntegerField(required=False, allow_null=True)  # ixtiyoriy
    full_name = serializers.CharField()
    phone = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    room_id = serializers.UUIDField()

    def validate(self, data):
        try:
            room = Room.objects.get(id=data.get('room_id'))
        except Room.DoesNotExist:
            raise serializers.ValidationError("Room not found!")
        data['room'] = room
        return data

    def create(self, validated_data):
        with transaction.atomic():
            # RoomOrder yaratish
            room_order = RoomOrder.objects.create(
                date=validated_data.get('date'),
                start_time=validated_data.get('start_time'),
                end_time=validated_data.get('end_time'),
                price=validated_data.get('price'),
                full_name=validated_data.get('full_name'),
                phone=validated_data.get('phone'),
                description=validated_data.get('description'),
                room=validated_data.get('room'),
                type='crm'
            )

            # Client yaratish yoki olish
            client, _ = Client.objects.get_or_create(
                phone=room_order.phone,
                defaults={
                    'name': room_order.full_name,
                    'status': 'new'
                }
            )

            # description bo‘lsa, ClientComment sifatida saqlash
            if room_order.description:
                ClientComment.objects.create(
                    client=client,
                    date=room_order.date,
                    comment=room_order.description
                )

            # IncomeCategory va Income
            category, _ = IncomeCategory.objects.get_or_create(name='Mijozlar')
            if room_order.price is not None:
                Income.objects.create(
                    category=category,
                    price=room_order.price,
                    date=room_order.date,
                )

            return room_order


class RoomOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomOrder
        fields = ['id', 'date', 'start_time', 'end_time', 'price', 'full_name', 'phone', 'description', 'type']
