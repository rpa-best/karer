from rest_framework.viewsets import ModelViewSet
from .models import Car
from .serializers import CarSerializer


class CarViewSet(ModelViewSet):
    http_method_names = ['head', 'get', 'post', 'patch']
    serializer_class = CarSerializer
    queryset = Car.objects.all().order_by('-id')
    search_fields = ['number', 'vin']
