from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _
from .models import ROLE_MANAGER, ROLE_LOGIST


class IsManagerUserPermission(BasePermission):
    message = _('User has not manager permission')

    def has_permission(self, request, view):
        return request.user.role == ROLE_MANAGER
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsLogistUserPermission(BasePermission):
    message = _('User has not logist permission')

    def has_permission(self, request, view):
        return request.user.role == ROLE_LOGIST
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
