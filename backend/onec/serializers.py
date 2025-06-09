from rest_framework import serializers

from .models import Nomenclature, Specification, Organization, Vehicle, Driver


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
        model = Vehicle
        fields = ["not_weight", "image"]


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = ["image"]
