from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views import invoice

router = DefaultRouter()
router.register('', invoice.InvoiceViewset, 'invoices')
router.register('(?P<invoice_id>\d+)/order/(?P<order_id>[0-9a-f-]+)/driver-comment', invoice.OrderDriverCommentViewset, 'order-driver-comments')
router.register('(?P<invoice_id>\d+)/order', invoice.OrderViewset, 'orders')
router.register('(?P<invoice_id>\d+)/available_nomenclature', invoice.AvailableNomenclatureViewset, 'available-nomenclatures')

urlpatterns = [
    path('', include(router.urls)),
    path('<invoice_id>/pivot/', invoice.InvoicePivotView.as_view(), name='invoice-pivot')
]
