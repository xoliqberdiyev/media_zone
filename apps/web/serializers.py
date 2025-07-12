from rest_framework import serializers

from apps.rooms.models import Room, RoomOrder, RoomImage


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
            'id', 'name', 'image', 'room_price_per_hour'
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
            'id', 'name', 'image', 'room_price_per_hour', 'room_images', 'room_orders'
        ]

