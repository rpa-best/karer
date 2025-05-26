from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewset, NomenclatureViewset, SpecificationViewset

router = DefaultRouter()
router.register('organization', OrganizationViewset, 'organization')
router.register('nomenclature', NomenclatureViewset, 'nomenclature')
router.register('specification', SpecificationViewset, 'specification')


urlpatterns = [
    path('', include(router.urls))
]