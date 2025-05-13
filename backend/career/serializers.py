from rest_framework import serializers

from car.serializers import CarSerializer
from driver.serializers import DriverSerializer
from invoice.models import Order
from invoice.serializers import InvoiceShowSerializer
from onec.serializers import NomenclatureSerializer


class OrderShowSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    driver = DriverSerializer()
    nomenclature = NomenclatureSerializer()
    invoice = InvoiceShowSerializer()

    class Meta:
        model = Order
        fields = "__all__"


class OrderPatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['fact']
