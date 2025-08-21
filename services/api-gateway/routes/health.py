from fastapi import APIRouter
from typing import Dict, Any


router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Health checkpoint to verify gateway is running"""
    return {
        "status": "healthy",
        "service": "API gateaway",
        "version": "1.0.0"
    }
