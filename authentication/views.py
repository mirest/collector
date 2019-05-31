from django.contrib.auth import login
from rest_framework import generics
from rest_framework.permissions import (DjangoModelPermissions, IsAdminUser,
                                        IsAuthenticated)
from rest_framework.response import Response
from social_core.exceptions import SocialAuthBaseException
from social_django.utils import load_backend, load_strategy

from authentication.models import User

from .serializer import SocialSerializer, TenantSerializer


class SocialAuthView(generics.CreateAPIView):
    serializer_class = SocialSerializer

    def post(self, request, backend, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            strategy = load_strategy(request)
            request.backend = load_backend(strategy, backend, None)
            user = request.backend.do_auth(
                serializer.validated_data['access_token'])
        except (SocialAuthBaseException) as e:
            return Response({"error": str(e)}, status=400)
        if user:
            login(request, user)
            serializer = TenantSerializer(user)
            return Response(serializer.data)
        return Response({"error": "unknown login error"}, status=400)


class UserView(generics.RetrieveAPIView):
    serializer_class = TenantSerializer
    permission_classes = (DjangoModelPermissions, IsAuthenticated)
    queryset = User.objects.none()

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class TenantsView(generics.ListAPIView):
    """Get all tenants
    """
    pagination_class = None
    serializer_class = TenantSerializer
    queryset = User.objects.filter(is_tenant=True)
    permission_classes = (DjangoModelPermissions, IsAdminUser)


class UsersView(generics.ListAPIView, generics.CreateAPIView):
    "Get all users"
    pagination_class = None
    queryset = User.objects.all()
    serializer_class = TenantSerializer
    permission_classes = (DjangoModelPermissions, IsAdminUser)
