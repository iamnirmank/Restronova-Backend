# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import InventoryApp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RestronovaRMS.settings')

# Define your WebSocket routing
websocket_application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            InventoryApp.routing.websocket_urlpatterns
        )
    ),
})

# Combine the HTTP and WebSocket applications
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": websocket_application,
})
