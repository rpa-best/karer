from django.db.models import Subquery, OuterRef, Sum
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from contrib.expressions import SumSubquery
from onec.models import Nomenclature, Price
from onec.serializers import NomenclatureSerializer
from career.tasks import send_to_career

from .. import serializers, filters
from ..models import Invoice, InvoiceNomenclature, Order, STATUS_CREATED, DriverComment


class InvoiceViewset(ModelViewSet):
    http_method_names = ['get', 'head', 'patch', 'post', 'delete']
    queryset = Invoice.objects.all().order_by('-created_at')
    filterset_class = filters.InvoiceFilter
    search_fields = ['id']
    ordering = ['-created_at', '-id']

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
    search_fields = ['car__number', 'address']
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(invoice_id=self.kwargs.get('invoice_id')).order_by('-created_at')

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

    @action(detail=True, methods=['post'])
    def send_career(self, request, *args, **kwargs):
        order: Order = self.get_object()
        send_to_career.delay(order.pk)
        return Response({'message': 'Заказ отправлен в Career'})


class OrderDriverCommentViewset(ModelViewSet):
    http_method_names = ['get', 'head', 'patch', 'post']
    serializer_class = serializers.OrderDriverCommentSerializer

    def get_queryset(self):
        return DriverComment.objects.filter(order_id=self.kwargs.get('order_id'))
    
    def create(self, request, *args, **kwargs):
        request.data.update(order=self.kwargs.get('order_id'))
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        request.data.update(order=self.kwargs.get('order_id'))
        return super().update(request, *args, **kwargs)


class AvailableNomenclatureViewset(ReadOnlyModelViewSet):
    serializer_class = NomenclatureSerializer

    def get_queryset(self):
        nids = InvoiceNomenclature.objects.filter(invoice_id=self.kwargs.get('invoice_id')).values_list('nomenclature_id', flat=True)
        return Nomenclature.objects.filter(uuid__in=nids).annotate(
            per_price=Subquery(
                Price.objects.filter(
                    nomenclature_id=OuterRef('uuid'),
                    specification_id=Subquery(Invoice.objects.filter(id=self.kwargs.get('invoice_id')).values('specification_id')[:1])
                ).values('price')[:1]
            )
        )


class InvoicePivotView(ListAPIView):
    serializer_class = NomenclatureSerializer

    def get_queryset(self):
        nomenclatures = InvoiceNomenclature.objects.filter(invoice_id=self.kwargs.get('invoice_id'))
        orders = Order.objects.filter(invoice_id=self.kwargs.get('invoice_id'))
        return Nomenclature.objects.filter(uuid__in=nomenclatures.values_list('nomenclature_id', flat=True)).annotate(
            fact=SumSubquery(nomenclatures.filter(nomenclature_id=OuterRef('uuid')), 'value'),
            fact_current=SumSubquery(orders.filter(nomenclature_id=OuterRef('uuid')), 'fact'),
            order_sum=SumSubquery(nomenclatures.filter(nomenclature_id=OuterRef('uuid')), 'value'),
            order_current_sum=SumSubquery(orders.filter(nomenclature_id=OuterRef('uuid')), 'order'),
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        invoice: Invoice = Invoice.objects.select_related('specification').get(id=self.kwargs.get('invoice_id'))
        return Response({
            'results': serializer.data,
            'summa': invoice.specification.amount_limit,
            'current_summa': Order.objects.filter(invoice_id=self.kwargs.get('invoice_id')).aggregate(sum=Sum('price')).get('sum')
        })
