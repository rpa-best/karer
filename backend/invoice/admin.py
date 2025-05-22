from django.contrib import admin
from .models import Invoice, InvoiceNomenclature, Order, DriverComment


class InvoiceNomenclatureInline(admin.TabularInline):
    model = InvoiceNomenclature
    extra = 0


class OrderInline(admin.StackedInline):
    model = Order
    extra = 0


class DriverCommentInline(admin.TabularInline):
    model = DriverComment
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['org', 'specification', 'status', 'type']
    list_filter = ['org', 'specification', 'type', 'status']
    inlines = [InvoiceNomenclatureInline, OrderInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'invoice', 'nomenclature', 'done']
    list_filter = ['invoice', 'nomenclature', 'done']
    search_fields = ['uuid']
    inlines = [DriverCommentInline]
