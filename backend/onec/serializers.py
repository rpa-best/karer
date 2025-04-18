from rest_framework import serializers

from .models import Nomenclature, Specification, Organization


class NomenclatureSerializer(serializers.ModelSerializer):
    per_price = serializers.FloatField(required=False)

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
