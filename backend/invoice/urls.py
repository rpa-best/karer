from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.InvoiceViewset, '')
router.register('(?P<invoice_id>\d+)/order', views.OrderViewset, '')
router.register('(?P<invoice_id>\d+)/available_nomenclature', views.AvailableNomenclatureViewset, '')

urlpatterns = [
    path('', include(router.urls))
]
