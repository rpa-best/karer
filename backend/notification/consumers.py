import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import Notification
from .serializers import NotificationSerializer

class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            f'notification_{self.scope["user"].id}',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            f'notification_{self.scope["user"].id}',
            self.channel_name
        )

    async def send_notification(self, event):
        message = event['message']
        await self.send_json(message)


def send_notification(notification: Notification):
    data = NotificationSerializer(notification).data
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notification_{notification.user_id}', {
            'type': 'send.notification',
            'message': json.loads(json.dumps(data)),
        }
    )