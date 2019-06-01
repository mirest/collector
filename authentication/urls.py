from django.urls import path

from .views import LoginView, SocialAuthView, TenantsView, UsersView, UserView

urlpatterns = [
    path('social/<str:backend>/', SocialAuthView.as_view(), name='login'),
    path('user', UserView.as_view(), name='user'),
    path('login', LoginView.as_view(), name='login'),
    path('tenants', UsersView.as_view(), name='tenants'),
    path('', TenantsView.as_view(), name='users'),
]
