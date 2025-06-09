from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from oauth.permissions import IsLogistUserPermission
from .serializers import OrganizationsSerializer, NomenclatureSerializer, SpecificationSerializer, CarSerializer, DriverSerializer
from .models import Organization, Nomenclature, Specification, Vehicle, Driver


class OrganizationViewset(ReadOnlyModelViewSet):
    serializer_class = OrganizationsSerializer
    queryset = Organization.objects.all()


class NomenclatureViewset(ReadOnlyModelViewSet):
    queryset = Nomenclature.objects.all()
    serializer_class = NomenclatureSerializer


class SpecificationViewset(ReadOnlyModelViewSet):
    serializer_class = SpecificationSerializer
    queryset = Specification.objects.all()


class CarViewSet(ModelViewSet):
    http_method_names = ['head', 'get', 'post', 'patch']
    serializer_class = CarSerializer
    queryset = Vehicle.objects.all().order_by('-created_at')
    search_fields = ['name', 'reg_number']
    permission_classes = [IsLogistUserPermission]


class DriverViewset(ModelViewSet):
    http_method_names = ['get', 'head', 'post', 'patch']
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()
    search_fields = ['name', 'telegram_id', 'phone_number']
    permission_classes = [IsLogistUserPermission]
