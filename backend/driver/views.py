from rest_framework.viewsets import ModelViewSet

from .serializers import DriverSerializer
from .models import Driver
from oauth.permissions import IsLogistUserPermission

class DriverViewset(ModelViewSet):
    http_method_names = ['get', 'head', 'post', 'patch']
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()
    search_fields = ['name', 'telegram_id']
    permission_classes = [IsLogistUserPermission]
