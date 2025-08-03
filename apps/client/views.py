from django.db.models import Prefetch

from rest_framework import generics, status, permissions, pagination
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.client import serializers, filter
from apps.client.models import Client, ClientComment


class ClientCreateApiView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = serializers.ClientCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientUpdateApiView(generics.UpdateAPIView):
    queryset = Client.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ClientUpdateSerializer
    lookup_field = 'id'


class ClientListApiView(generics.ListAPIView):
    queryset = Client.objects.prefetch_related(
        Prefetch('comments', queryset=ClientComment.objects.order_by('-created_at'))
    ).order_by('-created_at')
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ClientListSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = filter.ClientFilter