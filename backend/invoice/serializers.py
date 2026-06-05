from django.db.transaction import atomic
from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from onec.models import Specification
from onec.serializers import NomenclatureSerializer, CarSerializer, DriverSerializer
from .models import Invoice, InvoiceNomenclature, Order, TYPE_LIMIT, TYPE_PREPAYMENT, TYPE_DEFERMENT_PAYMENT, DriverComment 


class InvoiceNomenclatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceNomenclature
        fields = '__all__'


class InvoiceShowSerializer(serializers.ModelSerializer):
    nomenclatures = serializers.SerializerMethodField()
    number = serializers.CharField(read_only=True)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ['type', 'status']

    def get_nomenclatures(self, obj: Invoice):
        return InvoiceNomenclatureSerializer(InvoiceNomenclature.objects.filter(invoice=obj), many=True, context=self.context).data


class InvoiceSerializer(serializers.ModelSerializer):
    nomenclatures = serializers.ListField(write_only=True)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ['type', 'status']

    @atomic
    def create(self, validated_data):
        nomenclatures = validated_data.pop('nomenclatures', [])
        specification: Specification = validated_data.get('specification')
        if specification.amount_limit:
            validated_data['type'] = TYPE_LIMIT
        elif specification.payment_deferment:
            validated_data['type'] = TYPE_DEFERMENT_PAYMENT
        else:
            validated_data['type'] = TYPE_PREPAYMENT

        instance = super().create(validated_data)
        for nomenclature in nomenclatures:
            nomenclature['invoice'] = instance.pk
            serializer = InvoiceNomenclatureSerializer(
                data=nomenclature, context=self.context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return instance

    @atomic
    def update(self, instance, validated_data):
        nomenclatures = validated_data.pop('nomenclatures', [])
        instance = super().update(instance, validated_data)
        nomenclature_ids = []
        for nomenclature in nomenclatures:
            nomenclature['invoice'] = instance.pk
            if nomenclature.get('id'):
                n = get_object_or_404(
                    InvoiceNomenclature, id=nomenclature.get('id'))
                serializer = InvoiceNomenclatureSerializer(
                    n, nomenclature, context=self.context, partial=True)
            else:
                serializer = InvoiceNomenclatureSerializer(
                    data=nomenclature, context=self.context, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            nomenclature_ids.append(serializer.instance.pk)
        InvoiceNomenclature.objects.filter(invoice=instance).exclude(id__in=nomenclature_ids).delete()
        return instance


class OrderShowSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    driver = DriverSerializer()
    nomenclature = NomenclatureSerializer()

    class Meta:
        model = Order
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    new_driver_comment = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['driver_comment']

    def validate(self, attrs: dict):
        attrs = self._validate_invoice_value(attrs)
        attrs = self._validate_invoice_limit(attrs)
        attrs = self._validate_invoice_payment_deferment(attrs)
        return super().validate(attrs)
    
    def _validate_invoice_value(self, attrs: dict):
        invoice: Invoice = attrs.get('invoice')
        if attrs.get('order') is not None:
            agg_invoice = get_object_or_404(
                InvoiceNomenclature, invoice=invoice, nomenclature=attrs['nomenclature'])
            qs = Order.objects.filter(invoice=invoice, nomenclature=attrs['nomenclature'])
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            existing = qs.aggregate(norder=Sum('order'))['norder'] or 0
            if existing + attrs['order'] > agg_invoice.value:
                raise ValidationError(
                    f"Объём превышает лимит по заказу: {existing + attrs['order']} > {agg_invoice.value}"
                )
        return attrs

    def _validate_invoice_limit(self, attrs: dict):
        invoice: Invoice = attrs.get('invoice')
        limit = invoice.specification.amount_limit
        if attrs.get('price') is not None and limit:
            qs = Order.objects.filter(invoice=invoice)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            orders_price = qs.aggregate(price=Sum('price'))['price'] or 0
            if orders_price + attrs['price'] > limit:
                raise ValidationError(
                    f"Сумма заявок превышает лимит спецификации: {orders_price + attrs['price']} > {limit}"
                )
        return attrs

    def _validate_invoice_payment_deferment(self, attrs: dict):
        invoice: Invoice = attrs.get('invoice')
        if invoice.specification.payment_deferment:
            first_order = Order.objects.filter(invoice=invoice).order_by('created_at').first()
            if first_order and (timezone.now() - first_order.created_at).days > invoice.specification.payment_deferment:
                raise ValidationError("Срок создание заказа просрочен")
        return attrs

    def create(self, validated_data: dict):
        new_driver_comment = validated_data.pop('new_driver_comment', None)
        instance: Order = super().create(validated_data)
        if new_driver_comment:
            instance.send_driver_comment(new_driver_comment, self.context.get('request').user.id)
        return instance

    def update(self, instance, validated_data):
        new_driver_comment = validated_data.pop('new_driver_comment', None)
        instance: Order = super().update(instance, validated_data)
        if new_driver_comment:
            instance.send_driver_comment(new_driver_comment, self.context.get('request').user.id)
        return instance
    

class OrderDriverCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverComment
        fields = '__all__'

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.send_driver_comment(self.context.get('request').user.id)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.send_driver_comment(self.context.get('request').user.id)
        return instance
