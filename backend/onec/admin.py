from django.contrib import admin
from .models import Organization, Specification, Nomenclature, Price, Balance


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'inn', 'name']


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name']


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name', 'unit']


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['nomenclature', 'specification', 'price']
    list_filter = ['nomenclature', 'specification']


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['specification', 'balance']
    list_filter = ['specification']

