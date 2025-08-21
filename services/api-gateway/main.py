from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.health import router as health_router
from routes.api import router as api_router
from routes.websocket import router as ws_router

app = FastAPI(
    title="API gateway",
    description="app gateway to end user",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(api_router)
app.include_router(ws_router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "gateway API is running", "status": "healthy"}

