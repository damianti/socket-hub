from fastapi import APIRouter
from typing import Dict, Any
import sys
import os

# Add shared directory to path for logger import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from shared.logging import SocketHubLogger

# Create logger for health routes
logger = SocketHubLogger("chat-service").get_logger()

router = APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint"""
    logger.info("Health check requested")
    return {
        "service": "chat-service",
        "status": "healthy",
        "version": "1.0.0"
    }

@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check with service status"""
    logger.info("Detailed health check requested")
    
    # Here you would check database connections, external services, etc.
    # For now, we'll return basic status
    
    return {
        "service": "chat-service",
        "status": "healthy",
        "version": "1.0.0",
        "components": {
            "database": "healthy",
            "websocket": "healthy",
            "memory": "healthy"
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }

@router.get("/ready")
async def readiness_check() -> Dict[str, Any]:
    """Readiness check for Kubernetes/Docker"""
    logger.info("Readiness check requested")
    return {
        "status": "ready",
        "service": "chat-service"
    }

@router.get("/live")
async def liveness_check() -> Dict[str, Any]:
    """Liveness check for Kubernetes/Docker"""
    logger.info("Liveness check requested")
    return {
        "status": "alive",
        "service": "chat-service"
    }
