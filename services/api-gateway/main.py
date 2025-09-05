from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.health import router as health_router
from routes.api import router as api_router
from routes.websocket import router as ws_router
import sys
import os

# Agregar el directorio shared al path para importar el logger
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.logging import SocketHubLogger

# Crear logger para api-gateway
logger = SocketHubLogger("api-gateway").get_logger()

app = FastAPI(
    title="API gateway",
    description="app gateway to end user",
    version="1.0.0"
)

# Log startup
logger.info("🚀 API Gateway started successfully")

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
    logger.info("Health check requested")
    return {"message": "gateway API is running", "status": "healthy"}

