from django.db.transaction import atomic
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from onec.models import Specification
from car.serializers import CarSerializer
from driver.serializers import DriverSerializer
from onec.serializers import NomenclatureSerializer
from .models import Invoice, InvoiceNomenclature, Order, TYPE_LIMIT, TYPE_PREPAYMENT, TYPE_DEFERMENT_PAYMENT


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

    class Meta:
        model = Order
        fields = "__all__"

    def validate(self, attrs):
        invoice = attrs.get('invoice')
        agg_invoice = get_object_or_404(
            InvoiceNomenclature, invoice=invoice, nomenclature=attrs['nomenclature'])
        agg = Order.objects.filter(
            invoice=invoice,
            nomenclature=attrs['nomenclature']
        ).aggregate(norder=Sum('order'), nfact=Sum('fact'))
        if agg.get('order', 0) + attrs.get('order') > agg_invoice.value:
            raise ValidationError("Потрепность больше чем указано в инвоийс")
        return super().validate(attrs)
