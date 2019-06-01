from unittest.mock import patch

from tests.base import BaseTestCase

from .models import House


class TestHouse(BaseTestCase):

    def test_create_house_is_successfully_created(self):
        response = self.post_put_response('houses:create', self.house_data())
        self.assertEqual(201, response.status_code)

    def test_creating_house_fails(self):
        response = self.post_put_response('houses:create', {})
        self.assertEqual(400, response.status_code)

    def test_get_houses_succeeds(self):
        response = self.get_delete_response('houses:create')
        self.assertEqual(200, response.status_code)

    def test_get_not_paid_houses_succeeds(self):
        response = self.get_delete_response(
            'houses:create', query_kwargs={'is_paid': False})
        self.assertEqual(200, response.status_code)

    def test_get_paid_houses_succeeds(self):
        response = self.get_delete_response(
            'houses:create', query_kwargs={'is_paid': True})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), [])

    def test_get_single_house_succeeds(self):
        house_id = House.objects.first().identifier
        response = self.get_delete_response(
            'houses:crud', 'get', identifier=house_id)
        self.assertEqual(200, response.status_code)

    def test_update_single_house_succeeds(self):
        house_id = House.objects.first().identifier
        response = self.post_put_response(
            'houses:crud', data=self.house_data(is_occupied='true'),
            method='put', identifier=house_id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json()['is_occupied'], True)

    def test_delete_house_succeeds(self):
        house_id = House.objects.first().identifier
        response = self.get_delete_response('houses:crud',
                                            identifier=house_id,
                                            method='delete')
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), {'detail': 'successfully deleted'})

    def test_get_model_str(self):
        house = House.objects.first()
        assert house.__str__() == house.house_name

    @patch('houses.models.House.invoices')
    def test_get_model_is_paid(self, invoice):
        invoice.return_value = True
        house = House.objects.first()
        self.assertEqual(house.is_paid, True)

    @classmethod
    def house_data(self, **kwargs):
        data = {
            'house_name': "Simon Peter 25",
            'rate': 500000,
            **kwargs
        }
        return data
