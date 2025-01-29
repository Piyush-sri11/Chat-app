from django.urls import path , include
from server.consumers import ChatConsumer

# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
websocket_urlpatterns = [
    path("ws/<int:id>/" , ChatConsumer.as_asgi()) , 
]