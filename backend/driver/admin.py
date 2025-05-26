from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Driver

@admin.register(Driver)
class DriverAdmin(ModelAdmin):
    list_display = ('id', 'name', 'phone')
