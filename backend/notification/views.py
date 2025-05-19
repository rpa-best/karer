from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(ModelViewSet):
    http_method_names = ['get', 'head', 'patch']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Notification.objects.all()
        return Notification.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return NotificationSerializer
        return None

    def get_paginated_response(self, data):
        response: Response = super().get_paginated_response(data)
        response.data['unread'] = self.get_queryset().filter(read=False).count()
        return response

    def partial_update(self, request, *args, **kwargs):
        instance: Notification = self.get_object()
        instance.read_at = timezone.now()
        instance.read = True
        instance.save()
        return Response({'status': 'ok'})

    @action(['patch'], False)
    def read(self, request):
        queryset = self.get_queryset()
        queryset.update(read=True, read_at=timezone.now())
        return Response({'status': 'ok'})
    