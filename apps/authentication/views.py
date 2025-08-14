from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication import serializers, models

class CreateUserApiView(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer
    queryset = models.User.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated users to create accounts

    def perform_create(self, serializer):
        user = serializer.save()
        return Response({"success": True, "message": "User created successfully"}, status=status.HTTP_201_CREATED)

class UserApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CreateUserSerializer
    queryset = models.User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

class UserListApiView(generics.ListAPIView):
    serializer_class = serializers.CreateUserSerializer
    queryset = models.User.objects.exclude(role='admin')
    permission_classes = [permissions.IsAuthenticated]

class LoginApiView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    queryset = models.User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            token = RefreshToken.for_user(user)
            return Response({
                'access': str(token.access_token), 'refresh': str(token), 'role': user.role
            }, status=200)
        return Response(serializer.errors, status=400)