from datetime import datetime

from django.db.models import Q
from django_filters import FilterSet, rest_framework

from .models import House


class HouseFilter(FilterSet):
    is_occupied = rest_framework.BooleanFilter()
    start_date = rest_framework.DateFilter()
    is_paid = rest_framework.BooleanFilter(
        field_name='is_paid', method='filter_is_paid')

    class Meta:

        model = House
        fields = ('is_occupied', 'start_date', 'is_paid')

    def filter_is_paid(self, queryset, name, value):
        if value:
            query = {'invoices__end_date__gte': datetime.now().date()}
            return queryset.filter(**query).distinct()
        return queryset.filter(Q(
            invoices__end_date__lt=datetime.now().date()) | Q(
            invoices__isnull=True)).distinct()
