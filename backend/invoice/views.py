from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import ValidationError
from onec.models import Nomenclature
from onec.serializers import NomenclatureSerializer

from . import serializers
from .models import Invoice, InvoiceNomenclature, Order, STATUS_CREATED


class InvoiceViewset(ModelViewSet):
    http_method_names = ['get', 'head', 'patch', 'post', 'delete']
    queryset = Invoice.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return serializers.InvoiceSerializer           
        return serializers.InvoiceShowSerializer

    def perform_destroy(self, instance: Invoice):
        if instance.status in [STATUS_CREATED]:
            return super().perform_destroy(instance)
        raise ValidationError(f'Инвойс {instance} нельзя удалить')


class OrderViewset(ModelViewSet):
    http_method_names = ['get', 'head', 'patch', 'post', 'delete']

    def get_queryset(self):
        return Order.objects.filter(invoice_id=self.kwargs.get('invoice_id'))

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return serializers.OrderSerializer           
        return serializers.OrderShowSerializer

    def perform_destroy(self, instance: Order):
        if not instance.done:
            return super().perform_destroy(instance)
        raise ValidationError(f'Заказ {instance} нельзя удалить')
    
    def create(self, request, *args, **kwargs):
        request.data.update(invoice=self.kwargs.get('invoice_id'))
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        request.data.update(invoice=self.kwargs.get('invoice_id'))
        return super().update(request, *args, **kwargs)


class AvailableNomenclatureViewset(ReadOnlyModelViewSet):
    serializer_class = NomenclatureSerializer
    queryset = Nomenclature.objects

    def get_queryset(self):
        nids = InvoiceNomenclature.objects.filter(invoice_id=self.kwargs.get('invoice_id')).values_list('nomenclature_id', flat=True)
        return Nomenclature.objects.filter(uuid__in=nids)
