from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewset, NomenclatureViewset, SpecificationViewset

router = DefaultRouter()
router.register('organization', OrganizationViewset, '')
router.register('nomenclature', NomenclatureViewset, '')
router.register('specification', SpecificationViewset, '')


urlpatterns = [
    path('', include(router.urls))
]