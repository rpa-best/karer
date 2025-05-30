from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderView

router = DefaultRouter()
router.register('order', OrderView)

urlpatterns = [
    path('', include(router.urls))
]
