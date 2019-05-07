from django.urls import path

from .views import HouseView, SingleHouseView

urlpatterns = [
    path('', HouseView.as_view(), name='create'),
    path('<str:identifier>', SingleHouseView.as_view(),
         name='crud'),
]
