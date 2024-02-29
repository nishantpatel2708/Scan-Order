"""
ASGI config for reastaurant_management project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from django.core.asgi import get_asgi_application
from restaurant.consumers import WaiterCall
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reastaurant_management.settings')

application = get_asgi_application()

ws_pattern = [
    path('ws/waiter_call/<rest_id>', WaiterCall.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(URLRouter(
        ws_pattern
    ))
})