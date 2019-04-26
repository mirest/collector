from .payments import GeneratePaymentBatch
from dateutil.relativedelta import *
from payments.models import Invoices
from datetime import datetime
import math


def invoice_date_generator(instance, *args, **kwargs):
    # generate start and end_dates
    amount_paid = instance.amount_paid
    house_rate = instance.house.rate
    start_date = instance.house.start_date
    now = datetime.now().date()
    last_receipt = Invoices.objects.filter(
        payment_date__lte=now, house=instance.house,
        tenant=instance.tenant, is_deleted=False).first()

    start, end = generate_dates(
        amount_paid, house_rate, start_date, last_receipt)

    # update the instance
    instance.start_date = start
    instance.end_date = end
    # update house details if house is paid

    # return updated instance
    return instance


def generate_dates(amount_paid, house_rate, start_date, last_receipt):
    months = calculate_months(amount_paid, house_rate)
    if last_receipt:
        start = last_receipt.start_date or datetime.now().date()
    else:
        start = start_date if start_date else datetime.now().date()
    end = start + relativedelta(months=months)
    return start, end


def calculate_months(amount_paid, house_rate):
    return round_off(amount_paid/house_rate)


def round_off(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier
