from django.contrib import admin

from .models import Invoices


@admin.register(Invoices)
class InvoicesAdmin(admin.ModelAdmin):
    list_display = ["identifier"]
