from rest_framework import serializers

from apps.rooms.models import Room, RoomOrder, RoomImage
from apps.web.models import Image, Partner, Video


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
            'id', 'icon'
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

    
class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'id', 'video'
        ]