from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .models import ROLE_MANAGER, ROLE_LOGIST


class IsManagerUserPermission(IsAuthenticated):
    message = _('User has not manager permission')

    def has_permission(self, request, view):
        return request.user.role == ROLE_MANAGER and super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsLogistUserPermission(IsAuthenticated):
    message = _('User has not logist permission')

    def has_permission(self, request, view):
        return request.user.role == ROLE_LOGIST and super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
