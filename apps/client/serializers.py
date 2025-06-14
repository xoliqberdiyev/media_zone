from django.db import transaction

from rest_framework import serializers

from apps.client.models import Client


class ClientCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        with transaction.atomic():
            client = Client.objects.create(
                phone=validated_data.get('phone'),
                name=validated_data.get('name'),
                description=validated_data.get('description'),
                status='new',
            )
            return client
        return None
    

class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'name', 'phone', 'description', 'status'
        ]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.phone = validated_data.get('phone')
        instance.description = validated_data.get('description')
        instance.status = validated_data.get('status')
        return super().update(instance, validated_data)