from django.db import transaction
from rest_framework import serializers
from apps.client.models import Client, ClientComment

class ClientCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    comment = serializers.CharField(write_only=True)
    date = serializers.DateField(write_only=True)

    def validate_phone(self, value):
        if Client.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Client with this phone number already exists")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            client = Client.objects.create(
                phone=validated_data.get('phone'),
                name=validated_data.get('name'),
                status='new',
            )
            ClientComment.objects.create(
                client=client,
                comment=validated_data.get('comment'),
                date=validated_data.get('date')
            )
            return client

class ClientUpdateSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(required=False)
    date = serializers.DateField(required=False)

    class Meta:
        model = Client
        fields = [
            'name', 'phone', 'status', 'comment', 'date'
        ]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.phone = validated_data.get('phone')
        instance.status = validated_data.get('status')
        if validated_data.get('comment'):
            ClientComment.objects.create(
                client=instance,
                comment=validated_data.get('comment'),
                date=validated_data.get('date')
            )
        return super().update(instance, validated_data)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientComment
        fields = ['id', 'comment', 'date', 'created_at']

class ClientListSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Client
        fields = [
            'id', 'name', 'phone', 'status', 'back_color', 'comments'
        ]