from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Car

@admin.register(Car)
class CarAdmin(ModelAdmin):
    list_display = ('id', 'number', 'marka', 'model', 'vin', 'not_weight')
