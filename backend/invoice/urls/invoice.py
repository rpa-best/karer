from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import invoice

router = DefaultRouter()
router.register('', invoice.InvoiceViewset, '')
router.register('(?P<invoice_id>\d+)/order/(?P<order_id>[0-9a-f-]+)/driver-comment', invoice.OrderDriverCommentViewset, '')
router.register('(?P<invoice_id>\d+)/order', invoice.OrderViewset, '')
router.register('(?P<invoice_id>\d+)/available_nomenclature', invoice.AvailableNomenclatureViewset, '')

urlpatterns = [
    path('', include(router.urls)),
    path('<invoice_id>/pivot/', invoice.InvoicePivotView.as_view())
]
