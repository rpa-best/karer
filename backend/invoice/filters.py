import django_filters.rest_framework as filters

from invoice.models import Invoice


class InvoiceFilter(filters.FilterSet):
    status = filters.BaseInFilter(method='filter_status')

    class Meta:
        model = Invoice
        fields = ['org', 'status', 'specification', 'type']

    def filter_status(self, queryset, name, value: list):
        if not value or 'all' in value:
            return queryset
        return queryset.filter(status__in=value)
