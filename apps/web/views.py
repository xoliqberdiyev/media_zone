from rest_framework import generics

from apps.rooms import models as room_models
from apps.web import serializers, models


class RoomListApiView(generics.ListAPIView):
    queryset = room_models.Room.objects.prefetch_related('room_images') 
    serializer_class = serializers.RoomWebListSerializer


class RoomDetailApiView(generics.RetrieveAPIView):
    queryset = room_models.Room.objects.prefetch_related('room_images', 'room_orders') 
    serializer_class = serializers.RoomWebDetailSerializer
    lookup_field = 'id'


class PartnerListApiView(generics.ListAPIView):
    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnerListSerializer


class ImageListApiView(generics.ListAPIView):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageListSerializer
    

class VideoListApiView(generics.ListAPIView):
    queryset = models.Video.objects.only('id', 'video')
    serializer_class = serializers.VideoListSerializer
    

class TeamListApiView(generics.ListAPIView):
    queryset = models.Team.objects.only('id', 'name', 'image')
    serializer_class = serializers.TeamSerializer
    

class RoomOrderCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.RoomOrderWebSerializer
    queryset = room_models.RoomOrder.objects.all()