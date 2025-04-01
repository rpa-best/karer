from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from rest_framework import exceptions
from rest_framework_simplejwt.settings import api_settings
from .models import User


class AuthEmailSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        user = User.objects.filter(**{self.username_field: attrs[self.username_field]}).first()
        if not user.check_password(attrs["password"]):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        self.user = user
        data = {}
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class AuthUsernameSerializer(TokenObtainPairSerializer):
    username_field = "username"


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "role"]