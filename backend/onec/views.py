from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import OrganizationsSerializer, NomenclatureSerializer, SpecificationSerializer
from .models import Organization, Nomenclature, Specification


class OrganizationViewset(ReadOnlyModelViewSet):
    serializer_class = OrganizationsSerializer
    queryset = Organization.objects.all()


class NomenclatureViewset(ReadOnlyModelViewSet):
    queryset = Nomenclature.objects.all()
    serializer_class = NomenclatureSerializer


class SpecificationViewset(ReadOnlyModelViewSet):
    serializer_class = SpecificationSerializer
    queryset = Specification.objects.all()
