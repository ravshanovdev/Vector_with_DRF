
import os

from django.core.asgi import get_asgi_application

from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter

from channels.auth import AuthMiddlewareStack

from chats.consumers import PersonalChatConsumer, OnlineStatusConsumer, NotificationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whatsapp_clone.settings')

application = get_asgi_application()


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>/', PersonalChatConsumer),
            path('ws/online/', OnlineStatusConsumer),
            path('ws/notify/', NotificationConsumer)
        ])
    )
})