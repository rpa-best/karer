from rest_framework import serializers

from .models import Nomenclature, Specification, Organization, Car, Driver, Sender


class SenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sender
        fields = ['id', 'name']


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


_ONEC_DRIVER_FIELDS = {'name', 'inn', 'phone_number', 'job_title',
                       'drivers_license_series', 'drivers_license_number', 'sender'}


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = "__all__"

    def update(self, instance, validated_data):
        if instance.sender_id:
            for field in _ONEC_DRIVER_FIELDS:
                validated_data.pop(field, None)
        return super().update(instance, validated_data)
