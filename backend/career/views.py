from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet
from invoice.models import Order

from .serializers import OrderShowSerializer, OrderPatchSerializer


@extend_schema_view(
    list=extend_schema(tags=['career']),
    retrieve=extend_schema(tags=['career']),
    partial_update=extend_schema(tags=['career'])
)
class OrderView(ModelViewSet):
    http_method_names = ['get', 'patch']
    queryset = Order.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        if self.action in ["partial_update"]:
            return OrderPatchSerializer
        return OrderShowSerializer