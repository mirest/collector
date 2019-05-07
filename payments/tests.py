from tests.base import BaseTestCase

from .models import Invoices


class TestInvoices(BaseTestCase):

    def test_delete_invoice_is_successfully_created(self):
        invoice_id = Invoices.objects.first().identifier
        response = self.get_delete_response(
            'invoices:retrieve/update', identifier=invoice_id, method='delete')
        self.assertEqual(200, response.status_code)

    def test_create_invoice_fails_with_lower_amount(self):
        response = self.post_put_response(
            'invoices:create', self.get_invoice(amount_paid=10))
        self.assertEqual(400, response.status_code)

    def test_create_invoice_is_succesfull(self):
        response = self.post_put_response(
            'invoices:create', self.get_invoice())
        self.assertEqual(201, response.status_code)

    def get_invoice(self, **kwargs):
        invoice = {
            "amount_paid": 100000.0,
            "description": "new one",
            "payment_date": "2019-04-29",
            "invoice_no": "12342e31",
            "house": "b58d171f-0d01-458b-a953-c9dd0edb6c9c",
            "tenant": "2f7f8f92-4287-4f30-91b1-7aca9ab4fdaf",
            **kwargs
        }
        return invoice
