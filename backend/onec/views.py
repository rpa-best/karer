from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from oauth.permissions import IsLogistUserPermission
from .serializers import OrganizationsSerializer, NomenclatureSerializer, SpecificationSerializer, CarSerializer, DriverSerializer, SenderSerializer
from .models import Organization, Nomenclature, Specification, Car, Driver, Sender
from .filters import NomenclatureFilter, SpecificationFilter, OrganizationFilters


class SenderViewset(ReadOnlyModelViewSet):
    serializer_class = SenderSerializer
    queryset = Sender.objects.all()


class OrganizationViewset(ReadOnlyModelViewSet):
    serializer_class = OrganizationsSerializer
    filterset_class = OrganizationFilters

    def get_queryset(self):
        return Organization.objects.filter(specification__isnull=False)


class NomenclatureViewset(ReadOnlyModelViewSet):
    queryset = Nomenclature.objects.all()
    serializer_class = NomenclatureSerializer
    filterset_class = NomenclatureFilter


class SpecificationViewset(ReadOnlyModelViewSet):
    serializer_class = SpecificationSerializer
    queryset = Specification.objects.all()
    filterset_class = SpecificationFilter


class CarViewSet(ModelViewSet):
    http_method_names = ['head', 'get', 'post', 'patch']
    serializer_class = CarSerializer
    queryset = Car.objects.all().order_by('-created_at')
    search_fields = ['name', 'reg_number']
    permission_classes = [IsLogistUserPermission]


class DriverViewset(ModelViewSet):
    http_method_names = ['get', 'head', 'post', 'patch']
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()
    search_fields = ['name', 'telegram_id', 'phone_number']
    permission_classes = [IsLogistUserPermission]
