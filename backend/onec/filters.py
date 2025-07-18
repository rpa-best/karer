import django_filters.rest_framework as filters

from .models import Nomenclature, Specification


class NomenclatureFilter(filters.FilterSet):
    uuid = filters.BaseInFilter()

    class Meta:
        model = Nomenclature
        fields = ['uuid']


class SpecificationFilter(filters.FilterSet):

    class Meta:
        model = Specification
        fields = ['organization']
