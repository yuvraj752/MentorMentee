"""
ASGI config for MentorMentee project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from base.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MentorMentee.settings')

asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': asgi_app,
    'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
})
