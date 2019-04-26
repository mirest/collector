from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import Invoices
from .serializers import InvoicesSerializer


class InvoicesView(ListCreateAPIView):
    serializer_class = InvoicesSerializer
    queryset = Invoices.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('house__house_name', 'payment_date',)


class SingleInvoiceView(RetrieveUpdateDestroyAPIView):
    serializer_class = InvoicesSerializer
    queryset = Invoices.objects
    lookup_field = 'identifier'

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response({"detail": "successfully deleted"})
