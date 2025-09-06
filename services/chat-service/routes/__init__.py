# Import all routers for easy access
from .health import router as health_router
from .rooms import router as rooms_router
from .messages import router as messages_router
from .websocket import router as websocket_router

__all__ = [
    "health_router",
    "rooms_router", 
    "messages_router",
    "websocket_router"
]
