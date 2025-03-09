import os
from django.core.asgi import get_asgi_application
from decouple import config

# Set the default settings module using an environment variable,
# defaulting to development settings.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('DJANGO_SETTINGS_MODULE', default='config.settings.development'))

# Basic ASGI application for HTTP requests
application = get_asgi_application()

# ------------------------------------------------------------------------------
# If you plan to add asynchronous support (e.g., WebSockets) with Django Channels,
# you can update the ASGI application as follows.
#
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from api.routing import websocket_urlpatterns  # Define your websocket routes here
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })
# ------------------------------------------------------------------------------
