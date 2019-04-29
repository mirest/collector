from dateutil.relativedelta import *
from payments.models import Invoices
from datetime import datetime
from houses.models import House
import math


def invoice_date_generator(instance, *args, **kwargs):
    # generate start and end_dates
    amount_paid = instance.get('amount_paid')
    house_rate = instance.get('house').rate
    start_date = instance.get('house').start_date
    last_receipt = Invoices.objects.filter(date_created__lte=datetime.now(),
                                           house=instance.get('house'),
                                           tenant=instance.get('tenant'),
                                           is_deleted=False).last()
    start, end = generate_dates(
        amount_paid, house_rate, start_date, last_receipt)

    # update the instance
    instance['start_date'] = start
    instance['end_date'] = end
    # update house details if house is paid

    # update house
    tenant = instance['house'].tenant_id
    if not tenant or tenant != instance['tenant']:
        House.objects.filter(identifier=instance['house'].identifier).update(
            tenant_id=instance['tenant'], is_occupied=True)
    # return updated instance
    return instance


def generate_dates(amount_paid, house_rate, start_date, last_receipt):
    months = calculate_months(amount_paid, house_rate)
    if last_receipt is not None:
        start = last_receipt.end_date
    else:
        start = start_date if start_date else datetime.now().date()
    end = start + relativedelta(months=months)
    return start, end


def calculate_months(amount_paid, house_rate):
    return round_off(amount_paid/house_rate)


def round_off(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier
