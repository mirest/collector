from django.urls import path

from .views import SocialAuthView, TenantsView, UsersView, UserView

urlpatterns = [
    path('social/<str:backend>/', SocialAuthView.as_view(), name='login'),
    path('user', UserView.as_view(), name='user'),
    path('tenants', TenantsView.as_view(), name='tenants'),
    path('', UsersView.as_view(), name='users'),
]
