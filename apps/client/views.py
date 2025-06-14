from rest_framework import generics, status, permissions
from rest_framework.response import Response

from apps.client import serializers
from apps.client.models import Client


class ClientCreateApiView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = serializers.ClientCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientUpdateApiView(generics.UpdateAPIView):
    queryset = Client.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ClientUpdateSerializer
    lookup_field = 'id'