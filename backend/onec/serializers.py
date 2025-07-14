from rest_framework import serializers

from .models import Nomenclature, Specification, Organization, Car, Driver


class NomenclatureSerializer(serializers.ModelSerializer):
    per_price = serializers.FloatField(required=False)
    fact = serializers.FloatField(required=False)
    fact_current = serializers.FloatField(required=False)
    order_sum = serializers.FloatField(required=False)
    order_current_sum = serializers.FloatField(required=False)

    class Meta:
        model = Nomenclature
        fields = "__all__"


class SpecificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specification
        fields = "__all__"


class OrganizationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = "__all__"


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = "__all__"


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = "__all__"
