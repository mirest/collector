from django.db import models

from authentication.models import User
from utils.base_model import BaseModel
from datetime import datetime


class House(BaseModel):

    house_name = models.CharField(db_index=True, max_length=255, unique=True)

    rate = models.FloatField(blank=True)

    tenant_id = models.ForeignKey(
        User, unique=False, on_delete='CASCADE', blank=True, null=True,)

    owner_id = models.ForeignKey(
        User, unique=False, on_delete='CASCADE',
        related_name='landlord', blank=True, null=True)

    is_occupied = models.BooleanField(default=False)

    start_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.house_name

    @property
    def is_paid(self):
        invoice = self.invoices.filter(
            end_date__gte=datetime.now().date()).distinct()
        if invoice:
            return True
        return False
