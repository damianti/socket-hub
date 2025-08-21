from fastapi import APIRouter
from typing import Dict

router = APIRouter(
    prefix="/api",
    tags=["api gateway"]
)

@router.get("/")
def read_root()-> Dict[str, str]:
    return {
        "message": "API gateway is running",
        "docs": "/docs"
    }

