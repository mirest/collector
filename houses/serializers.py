from rest_framework import serializers
from .models import House


class HouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = House
        fields = ('identifier','house_name','rate','is_occupied','start_date','tenant_id','owner_id')