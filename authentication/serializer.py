from rest_framework import serializers

from .models import User


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )


class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('identifier', 'email', 'username', 'name', 'phonenumber',
                  'is_staff', 'is_admin', 'is_tenant', 'is_landlord')
        extra_kwargs = {'identifier': {'read_only': True},
                        'name': {'required': True}}
