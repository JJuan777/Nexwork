# NexworkApp/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server/(?P<conversacion_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
