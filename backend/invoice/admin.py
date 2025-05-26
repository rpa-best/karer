from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from .models import Invoice, InvoiceNomenclature, Order, DriverComment


class InvoiceNomenclatureInline(TabularInline):
    model = InvoiceNomenclature
    extra = 0


class OrderInline(StackedInline):
    model = Order
    extra = 0


class DriverCommentInline(TabularInline):
    model = DriverComment
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    list_display = ['org', 'specification', 'status', 'type']
    list_filter = ['org', 'specification', 'type', 'status']
    inlines = [InvoiceNomenclatureInline, OrderInline]


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['uuid', 'invoice', 'nomenclature', 'done']
    list_filter = ['invoice', 'nomenclature', 'done']
    search_fields = ['uuid']
    inlines = [DriverCommentInline]
