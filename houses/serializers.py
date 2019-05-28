from rest_framework import serializers
from .models import House
from authentication.serializer import TenantSerializer


class HouseSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(source='tenant_id', read_only=True)
    owner = TenantSerializer(source='owner_id', read_only=True)

    class Meta:
        model = House
        fields = ('identifier', 'house_name', 'rate', 'is_occupied',
                  'start_date', 'tenant_id', 'owner_id', 'tenant', 'is_paid',
                  'owner', 'invoices')
        extra_kwargs = {'tenant_id': {'write_only': True, 'required': False},
                        'owner_id': {'write_only': True, 'required': False},
                        'invoices': {'read_only': True}}
