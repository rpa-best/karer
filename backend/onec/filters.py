import django_filters.rest_framework as filters

from .models import Nomenclature, Specification, Organization, Driver


class OrganizationFilters(filters.FilterSet):

    class Meta:
        model = Organization
        fields = ['sender']


class NomenclatureFilter(filters.FilterSet):
    uuid = filters.BaseInFilter()

    class Meta:
        model = Nomenclature
        fields = ['uuid']


class SpecificationFilter(filters.FilterSet):

    class Meta:
        model = Specification
        fields = ['organization']


class DriverFilter(filters.FilterSet):

    class Meta:
        model = Driver
        fields = ['sender']
