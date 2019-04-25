from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import HouseView,SingleHouseView

urlpatterns = [
    path('', HouseView.as_view(),name='create'),
    path('<str:identifier>', SingleHouseView.as_view(),name='retrieve/update'),
]
