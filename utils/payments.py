import sys
from datetime import datetime

from dateutil.relativedelta import *


class GeneratePaymentBatch():
    payments = None

    def __init__(self, payments, instance):
        self.payments = payments.all()
        self.instance = instance

    def get_batch(self):
        return self.get_last_payment()

    def get_last_payment(self):
        if self.payments.count() > 0:
            batch = self.update_last_batch()
        else:
            batch = self.create_payment_batch()
        return batch

    def create_payment_batch(self):
        due_date, kwargs = self.get_due_date()
        batch = self.payments.create(
            house_id=self.instance.house,
            tenant_id=self.instance.house.tenant_id,
            due_date=due_date)
        if kwargs.get('excess'):
            next_batch = self.generate_new_batch(
                kwargs.get('excess'), due_date)
        return batch

    def get_due_date(self, last_date=None, **kwargs):
        months = self.instance.amount_paid / self.instance.house.rate
        if not last_date:
            date = self.instance.house.start_date + \
                relativedelta(months=int(months))
        else:
            date = last_date + relativedelta(months=int(months))
        if not months.is_integer():
            excess = (self.instance.amount_paid %
                      self.instance.house.rate)
            kwargs['excess'] = excess
            self.instance.amount_paid = self.instance.amount_paid - excess

        return date, kwargs

    def update_last_batch(self):
        batch = self.payments.last()
        due_date, kwargs = self.get_due_date(last_date=batch.due_date)
        batch.due_date = due_date
        batch.save()
        if kwargs.get('excess'):
            next_batch = self.generate_new_batch(
                kwargs.get('excess'), due_date)
        return batch

    def generate_new_batch(self, excess, due_date):
        next_batch = self.payments.create(
            house_id=self.instance.house,
            tenant_id=self.instance.house.tenant_id,
            due_date=due_date+relativedelta(months=1))

        return next_batch