from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response

from .filters import HouseFilter
from .models import House
from .serializers import HouseSerializer


class HouseView(ListCreateAPIView):
    """
    Create and list Houses view
    """
    serializer_class = HouseSerializer
    queryset = House.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    permission_classes = (DjangoModelPermissions, IsAuthenticated)
    filter_class = HouseFilter
    search_fields = ('tenant_id__name','house_name','rate','tenant_id__email')


class SingleHouseView(RetrieveUpdateDestroyAPIView):
    serializer_class = HouseSerializer
    queryset = House.objects
    permission_classes = (DjangoModelPermissions, IsAuthenticated)
    lookup_field = 'identifier'

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)  # noqa
        return Response({"detail": "successfully deleted"})
