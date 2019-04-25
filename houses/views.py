from rest_framework.generics import ListCreateAPIView
from .serializers import HouseSerializer
from .models import House

class HouseView(ListCreateAPIView):
    serializer_class = HouseSerializer
    queryset = House.objects.all()
    