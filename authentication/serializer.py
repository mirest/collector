from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(
        max_length=128, write_only=True, required=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        validated_data = super().validate(data)
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password'])

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token,
        }

    def create(self, validated_data):
        return validated_data


class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('identifier', 'email', 'username', 'name', 'phonenumber',
                  'is_staff', 'is_admin', 'is_tenant', 'is_landlord')
        extra_kwargs = {'identifier': {'read_only': True},
                        'name': {'required': True}}
