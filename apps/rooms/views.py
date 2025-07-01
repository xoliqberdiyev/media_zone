from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions

from apps.rooms import serializers, models
from apps.shared.pagination import CustomPageNumberPagination


class RoomListApiView(generics.ListAPIView):
    serializer_class = serializers.RoomListSerializer
    queryset = models.Room.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class RoomOrderCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.RoomOrderCreateSerializer
    queryset = models.RoomOrder.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class RoomOrderListSerializer(generics.ListAPIView):
    serializer_class = serializers.RoomOrderListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        room = get_object_or_404(models.Room, id=self.kwargs.get('room_id'))
        return models.RoomOrder.objects.filter(room=room)