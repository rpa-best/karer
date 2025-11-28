from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Organization, Specification, Nomenclature, Price, Balance, Sender


@admin.register(Sender)
class SenderAdmin(ModelAdmin):
    list_display = ['name', 'url']


@admin.register(Organization)
class OrganizationAdmin(ModelAdmin):
    list_display = ['uuid', 'inn', 'name']


@admin.register(Specification)
class SpecificationAdmin(ModelAdmin):
    list_display = ['uuid', 'name']


@admin.register(Nomenclature)
class NomenclatureAdmin(ModelAdmin):
    list_display = ['uuid', 'name', 'unit']


@admin.register(Price)
class PriceAdmin(ModelAdmin):
    list_display = ['nomenclature', 'specification', 'price']
    list_filter = ['nomenclature', 'specification']


@admin.register(Balance)
class BalanceAdmin(ModelAdmin):
    list_display = ['specification', 'balance']
    list_filter = ['specification']

