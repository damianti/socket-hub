from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import httpx
import os
from typing import Dict

router = APIRouter(
    prefix="/api",
    tags=["api gateway"]
)

AUTH_SERVICE_URL =  os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")

@router.get("/")
def read_root()-> Dict[str, str]:
    return {
        "message": "API gateway is running",
        "docs": "/docs"
    }
@router.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_proxy(request: Request, path: str):
    
    target_url = f"{AUTH_SERVICE_URL}/auth/{path}"
    body = await request.body()
    headers = dict (request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=request.query_params
        )
    return StreamingResponse(
        content=response.aiter_bytes(),
        status_code=response.status_code,
        headers=dict(response.headers)
    )
    