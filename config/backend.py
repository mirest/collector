import jwt
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from social_core.exceptions import MissingBackend
from social_django.utils import load_backend, load_strategy

from authentication.models import User
from config.default import SECRET_KEY


class SocialAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = get_authorization_header(
            request).decode(HTTP_HEADER_ENCODING)
        auth = auth_header.split()

        if not auth or auth[0].lower() != 'bearer':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No backend provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) == 2:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 3:
            msg = 'Invalid token header. Token string should not contain spaces.'  # noqa
            raise exceptions.AuthenticationFailed(msg)

        token = auth[2]
        backend = auth[1]

        strategy = load_strategy(request=request)

        try:
            backend = load_backend(strategy, backend, None)
        except MissingBackend:
            msg = 'Invalid token header. Invalid backend.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = backend.do_auth(access_token=token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))

        if not user:
            msg = 'Bad credentials.'
            raise exceptions.AuthenticationFailed(msg)
        return user, token

    def authenticate_header(self, request):
        """
        Bearer is the only finalized type currently
        """
        return 'Bearer backend realm="%s"' % 'api'


class JWTAuthentication(BaseAuthentication):
    authentication_header_prefix = 'bearer'

    def authenticate(self, request):
        auth = get_authorization_header(
            request).decode(HTTP_HEADER_ENCODING)
        auth_headers = auth.split()
        if not auth_headers:
            return None

        if len(auth_headers) == 1 or len(auth_headers) > 2:
            return None
        prefix = auth_headers[0]
        token = auth_headers[1]
        if prefix.lower() != self.authentication_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, SECRET_KEY)
        except jwt.InvalidTokenError or jwt.DecodeError:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        except jwt.ExpiredSignature:
            msg = 'Token has expired. please login again'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(username=payload['username'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        return (user, token)
