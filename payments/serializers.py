from rest_framework import serializers
from .models import Invoices
from utils.signals import invoice_date_generator


class InvoicesSerializer(serializers.ModelSerializer):
    amount_paid = serializers.FloatField()

    class Meta:
        model = Invoices
        exclude = ('updated_at', 'deleted_at', 'is_deleted',)
        extra_kwargs = {'start_date': {'read_only': True},
                        'end_date': {'read_only': True}}

    def create(self, validated_data):
        updated_data = invoice_date_generator(validated_data)
        instance = super().create(updated_data)
        return instance

    def validate(self, data):
        amount_paid = data.get('amount_paid')
        rate = data.get('house').rate
        if amount_paid % rate != 0:
            raise serializers.ValidationError(
                f'The amount paid should be in multiples of the house rate(UGX{rate})')  # noqa
        return super().validate(data)
