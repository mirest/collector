from django.contrib import admin

from houses.models import House

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phonenumber', 'name']
    prepopulated_fields = {'username': ('email', 'phonenumber',)}


@admin.register(House)
class HousesAdmin(admin.ModelAdmin):
    list_display = ['house_name', 'rate', 'tenant_id', 'owner_id']
    list_filter = ['date_created']
    search_fields = ['house_name', 'name']
