import django_filters.rest_framework as filters

from invoice.models import Order


class OrderFilter(filters.FilterSet):
    updated_at__gte = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_at__lte = filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['updated_at__gte', 'updated_at__lte']
