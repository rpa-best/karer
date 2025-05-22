from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'severity', 'created_at', 'read_at', 'read')
    list_filter = ('read', 'user', 'severity')
    search_fields = ('label', 'message')

