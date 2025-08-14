from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from apps.authentication import models


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = models.User.objects.filter(username=data['username']).first()
        if not user:
            raise serializers.ValidationError('User not found')
        if not user.check_password(data['password']):
            raise serializers.ValidationError('User not found')
        data['user'] = user
        return data


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'username', 'password']
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