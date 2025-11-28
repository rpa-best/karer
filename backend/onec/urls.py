from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewset, NomenclatureViewset, SpecificationViewset, CarViewSet, DriverViewset, SenderViewset

router = DefaultRouter()
router.register('sender', SenderViewset, 'sender')
router.register('organization', OrganizationViewset, 'organization')
router.register('nomenclature', NomenclatureViewset, 'nomenclature')
router.register('specification', SpecificationViewset, 'specification')
router.register('car', CarViewSet, 'car')
router.register('driver', DriverViewset, 'driver')

urlpatterns = [
    path('', include(router.urls))
]