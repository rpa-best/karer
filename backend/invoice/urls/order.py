from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ..views.order import OrderViewSet

router = DefaultRouter()

router.register('', OrderViewSet, 'orders')


urlpatterns = [
    path('', include(router.urls))
]