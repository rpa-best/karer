from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ('id', 'label', 'severity', 'created_at', 'read_at', 'read')
    list_filter = ('read', 'user', 'severity')
    search_fields = ('label', 'message')

