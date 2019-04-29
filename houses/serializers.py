from rest_framework import serializers
from .models import House
from authentication.serializer import UserSerializer
from payments.serializers import InvoicesSerializer


class HouseSerializer(serializers.ModelSerializer):
    tenant = UserSerializer(source='tenant_id', read_only=True)
    owner = UserSerializer(source='owner_id', read_only=True)

    class Meta:
        model = House
        fields = ('identifier', 'house_name', 'rate', 'is_occupied',
                  'start_date', 'tenant_id', 'owner_id', 'tenant', 'is_paid',
                  'owner', 'invoices')
        extra_kwargs = {'tenant_id': {'write_only': True, 'required': False},
                        'owner_id': {
            'write_only': True, 'required': False}}
