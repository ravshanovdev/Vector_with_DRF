from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<id>\d+)/(?P<chat_id>\w+)/$', consumers.ChatPersonalConsumer.as_asgi()),
]
