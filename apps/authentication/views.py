from rest_framework import generics, permissions

from apps.authentication import serializers, models


class CreateUserApiView(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer
    queryset = models.User.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class UserApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CreateUserSerializer
    queryset = models.User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

class UserListApiView(generics.ListAPIView):
    serializer_class = serializers.CreateUserSerializer
    queryset = models.User.objects.exclude(role='admin')
    permission_classes = [permissions.IsAuthenticated]