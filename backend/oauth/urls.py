from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AuthView


urlpatterns = [
    path("auth/", AuthView.as_view()),
    path("refresh-token/", TokenRefreshView.as_view())
]
