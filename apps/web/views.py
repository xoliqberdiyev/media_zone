from rest_framework import generics

from apps.rooms import models
from apps.web import serializers



class RoomListApiView(generics.ListAPIView):
    queryset = models.Room.objects.prefetch_related('room_images') 
    serializer_class = serializers.RoomWebListSerializer


class RoomDetailApiView(generics.RetrieveAPIView):
    queryset = models.Room.objects.prefetch_related('room_images', 'room_orders') 
    serializer_class = serializers.RoomWebDetailSerializer
    lookup_field = 'id'