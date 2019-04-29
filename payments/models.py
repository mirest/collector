from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, pre_save

from authentication.models import User
from houses.models import House
from utils.base_model import BaseModel


class Invoices(BaseModel):

    amount_paid = models.FloatField(blank=True)

    description = models.CharField(max_length=255)

    payment_date = models.DateField(auto_now=True, null=True)

    start_date = models.DateField(blank=True, null=True)

    end_date = models.DateField(blank=True, null=True)

    invoice_no = models.CharField(max_length=255, blank=True)

    house = models.ForeignKey(
        House, unique=False, on_delete='CASCADE', null=False,
        related_name='invoices')

    tenant = models.ForeignKey(
        User, unique=False, on_delete='CASCADE', related_name='tenant')