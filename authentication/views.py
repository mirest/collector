from django.contrib.auth import login
from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from social_django.utils import load_backend, load_strategy

from authentication.models import User

from .serializer import SocialSerializer, UserSerializer


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
        except Exception as e:
            return Response({"error": str(e)})
        if user:
            login(request, user)
            return Response({'email': user.email,
                             'username': user.username
                             })
        return Response({"error": "unknown login error"})


class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (DjangoModelPermissions,)
    queryset = User.objects.none()

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class UsersView(generics.ListAPIView):
    """Get all tenants
    """
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_tenant=True)


class TenantsView(UsersView):
    "Get all users"
    pagination_class = None
