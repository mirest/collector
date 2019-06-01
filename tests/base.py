import json

from django.test import TestCase
from django.urls import reverse as django_reverse
from django.utils.http import urlencode
from rest_framework.test import APIClient

from authentication.models import User


class BaseTestCase(TestCase):
    fixtures = ['fixtures/users.json', 'fixtures/houses.json',
                'fixtures/payments.json']

    def setUp(self):
        self.client = APIClient()
        user = User.objects.get(username='kimbugp')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + user.token())

    def post_put_response(self, url_name, data, method='post', **kwargs):
        self.assertIn(method, ['post', 'put'], msg=(
            'only post and put methods are allowed'))
        response = self.client.__getattribute__(method)(
            reverse(url_name, kwargs=kwargs),
            content_type='application/json',
            data=json.dumps(data))
        return response

    def get_delete_response(self, url_name, method='get', query_kwargs=None, **kwargs):  # noqa
        self.assertIn(method, ['get', 'delete'], msg=(
            'only get and delete methods are allowed'))
        response = self.client.__getattribute__(method)(
            reverse(url_name, kwargs=kwargs, query_kwargs=query_kwargs),
            content_type='application/json')
        return response


def reverse(urlname, kwargs=None, query_kwargs=None):
    url = django_reverse(urlname, kwargs=kwargs)
    if query_kwargs:
        return u'%s?%s' % (url, urlencode(query_kwargs))

    return url
