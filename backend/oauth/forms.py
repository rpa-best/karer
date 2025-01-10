import unicodedata
from django.contrib.auth.forms import UserCreationForm as _UserCreationForm, UsernameField as _UsernameField, UserChangeForm as _UserChangeForm
from .models import User


class UsernameField(_UsernameField):
    def to_python(self, value):
        return unicodedata.normalize("NFKC", value) if value else value


class UserCreationForm(_UserCreationForm):
    
    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {"username": UsernameField, "email": UsernameField}


class UserChangeForm(_UserChangeForm):

    class Meta:
        model = User
        fields = "__all__"
        field_classes = {"username": UsernameField, "email": UsernameField}