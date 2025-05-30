"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from notification.routing import websocket_urlpatterns as invoice
from contrib.websocket import WebsocketMiddlewareStack

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": WebsocketMiddlewareStack(
        URLRouter([
            *invoice
        ])
    ),
})