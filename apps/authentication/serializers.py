from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from apps.authentication import models


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id','first_name', 'last_name', 'username', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = models.User.objects.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data.get('username'),
        )
        user.set_password(validated_data.get('password'))
        user.role = 'operator'
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        if validated_data.get('password'):
            instance.password = make_password(validated_data.get('password'))
        instance.save()
        return instance