from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
import json


class BaseTestCase(TestCase):
    fixtures = ['fixtures/users.json', 'fixtures/houses.json',
                'fixtures/payments.json']

    def setUp(self):
        self.client = APIClient()

    def post_put_response(self, url_name, data, method='post', **kwargs):
        response = self.client.__getattribute__(method)(
            reverse(url_name, kwargs=kwargs),
            content_type='application/json',
            data=json.dumps(data))
        return response

    def get_delete_response(self, url_name, method='get', **kwargs):
        response = self.client.__getattribute__(method)(
            reverse(url_name, kwargs=kwargs),
            content_type='application/json')
        return response
