from django.db import transaction

from rest_framework import serializers

from apps.rooms.models import Room, RoomOrder, RoomImage
from apps.web.models import Image, Partner, Video, Team
from apps.client.models import Client
from apps.finance.models import Income, IncomeCategory


class ListRoomImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = [
            'id', 'image'
        ]


class RoomWebListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'id', 'name_uz', 'name_ru', 'image', 'description_uz', 'description_ru', 'room_price_per_hour'
        ]


class RoomWebOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomOrder
        fields = '__all__'


class RoomWebDetailSerializer(serializers.ModelSerializer):
    room_images = ListRoomImagesSerializer(many=True)
    room_orders = RoomWebOrderListSerializer(many=True)

    class Meta:
        model = Room
        fields = [
            'id', 'name_uz', 'name_ru', 'image', 'description_uz', 'description_ru', 'room_price_per_hour', 'room_images', 'room_orders'
        ]

    
class PartnerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner 
        fields = [
            'id', 'icon', 'instagram_link'
        ]



class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image 
        fields = [
            'id', 'image'
        ]

    
class RoomOrderWebSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomOrder
        fields = [
            'full_name', 'phone', 'date', 'start_time', 'end_time', 'price', 'description', 'room'
        ]

    def create(self, validated_data):
        with transaction.atomic():
            room = RoomOrder.objects.create(
                date=validated_data.get('date'),
                start_time=validated_data.get('start_time'),
                end_time=validated_data.get('end_time'),
                price=validated_data.get('price'),
                full_name=validated_data.get('full_name'),
                phone=validated_data.get('phone'),
                description=validated_data.get('description'),
                room=validated_data.get('room'),
                type='web'
            )
            Client.objects.get_or_create(
                phone=room.phone,
                name=room.full_name,
                description=room.description,
                status='new',
            )
            category, _ = IncomeCategory.objects.get_or_create(name='Mijozlar')
            Income.objects.create(
                category=category,
                price=room.price,
                date=room.date,
            )
            return room


class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'id', 'video'
        ]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team 
        fields = [
            'id', 'name', 'image'
        ]