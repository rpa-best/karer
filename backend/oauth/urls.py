from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AuthView, MeView


urlpatterns = [
    path("auth/", AuthView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", MeView.as_view()),
]
