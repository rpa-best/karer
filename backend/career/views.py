from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet
from invoice.models import Order
from onec.tasks import send_order_onec
from .filters import OrderFilter
from .serializers import OrderShowSerializer, OrderPatchSerializer


@extend_schema_view(
    list=extend_schema(tags=['career']),
    retrieve=extend_schema(tags=['career']),
    partial_update=extend_schema(tags=['career'])
)
class OrderView(ModelViewSet):
    http_method_names = ['get', 'patch']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter

    def get_queryset(self):
        return Order.objects.filter(fact__isnull=True)

    def get_serializer_class(self):
        if self.action in ["partial_update"]:
            return OrderPatchSerializer
        return OrderShowSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.done = True
        instance.save(update_fields=['done'])
        send_order_onec(instance.pk)