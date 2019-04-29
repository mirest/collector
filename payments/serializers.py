from rest_framework import serializers
from .models import Invoices
from utils.signals import invoice_date_generator


class InvoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoices
        exclude = ('updated_at', 'deleted_at', 'is_deleted',)
        extra_kwargs = {'start_date': {
            'read_only': True}, 'end_date': {'read_only': True}}

    def create(self, validated_data):
        updated_data = invoice_date_generator(validated_data)
        instance = super().create(updated_data)
        return instance
