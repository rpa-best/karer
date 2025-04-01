from django.db.transaction import atomic
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import Invoice, InvoiceNomenclature, Order


class InvoiceNomenclatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceNomenclature
        fields = '__all__'


class InvoiceShowSerializer(serializers.ModelSerializer):
    nomenclatures = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ['type', 'status']

    def get_nomenclatures(self, obj: Invoice):
        return InvoiceNomenclatureSerializer(InvoiceNomenclature.objects.filter(invoice=obj), many=True, context=self.context).data


class InvoiceSerializer(serializers.ModelSerializer):
    nomenclatures = InvoiceNomenclatureSerializer(many=True)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ['type', 'status']

    @atomic
    def create(self, validated_data):
        nomenclatures = validated_data.pop('nomenclatures', [])
        instance = super().create(validated_data)
        for nomenclature in nomenclatures:
            nomenclature['invoice'] = instance.pk
            serializer = InvoiceNomenclatureSerializer(
                data=nomenclature, context=self.context)
            serializer.is_valid(True)
            serializer.save()
        return instance

    @atomic
    def update(self, instance, validated_data):
        nomenclatures = validated_data.pop('nomenclatures', [])
        instance = super().update(instance, validated_data)
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
            serializer.is_valid(True)
            serializer.save()
        return instance


class OrderShowSerializer(serializers.ModelSerializer):

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
        if (agg.get('order', 0) + attrs.get('order') > agg_invoice.value):
            raise ValidationError("Потрепность больше чем указано в инвоийс")
        return super().validate(attrs)
