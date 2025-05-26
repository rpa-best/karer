from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DriverViewset

router = DefaultRouter()
router.register('', DriverViewset, 'drivers')

urlpatterns = [
    path('', include(router.urls))
]
