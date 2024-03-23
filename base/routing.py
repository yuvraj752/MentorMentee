from django.urls import path
from .consumers import Chat

websocket_urlpatterns = [
    path('ws/chat/', Chat.as_asgi())
]