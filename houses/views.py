from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.db.models.query import QuerySet


from .serializers import HouseSerializer
from .models import House


class HouseView(ListCreateAPIView):
    """
    Create and list Houses view
    """
    serializer_class = HouseSerializer
    queryset = House.objects.all()


class SingleHouseView(RetrieveUpdateDestroyAPIView):
    serializer_class = HouseSerializer
    queryset = House.objects
    lookup_field = 'identifier'

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response({"detail": "successfully deleted"})
