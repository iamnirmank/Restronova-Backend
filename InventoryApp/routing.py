# routing.py
from django.urls import path
from .consumers import Consumer

websocket_urlpatterns = [
    path('ws/websocket/', Consumer.as_asgi()),
    ]