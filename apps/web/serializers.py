from rest_framework import serializers

from rooms.models import Room, RoomOrder


class BaseRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'id', 'name', 'room_image'
        ]