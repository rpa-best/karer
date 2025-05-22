from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from invoice.models import Order
from .. import serializers
from oauth.permissions import IsLogistUserPermission

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'head', 'patch', 'delete']
    search_fields = ['car__number', 'address']
    ordering = ['-created_at']
    permission_classes = [IsLogistUserPermission]

    def get_queryset(self):
        return Order.objects.order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return serializers.OrderSerializer
        return serializers.OrderShowSerializer

    def perform_destroy(self, instance: Order):
        if not instance.done:
            return super().perform_destroy(instance)
        raise ValidationError(f'Заказ {instance} нельзя удалить')

    def update(self, request, *args, **kwargs):
        request.data.update(invoice=self.kwargs.get('invoice_id'))
        return super().update(request, *args, **kwargs)
