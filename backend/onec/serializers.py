from rest_framework import serializers

from .models import Nomenclature, Specification, Organization


class NomenclatureSerializer(serializers.ModelSerializer):

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
