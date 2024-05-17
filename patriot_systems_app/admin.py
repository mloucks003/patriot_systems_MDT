from django.contrib import admin
from .models import Civilian, Vehicle

class CivilianAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    search_fields = ['name']

class VehicleAdmin(admin.ModelAdmin):
    list_display = ['license_plate', 'make', 'model', 'year', 'color', 'is_insurance_valid', 'is_registration_valid', 'owner']
    search_fields = ['license_plate', 'make', 'owner__name']
    list_filter = ['make', 'model', 'year', 'is_insurance_valid', 'is_registration_valid']
    raw_id_fields = ['owner']

admin.site.register(Civilian, CivilianAdmin)
admin.site.register(Vehicle, VehicleAdmin)
