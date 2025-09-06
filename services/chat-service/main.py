from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys
import os

# Add shared directory to path for logger import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.logging import SocketHubLogger

# Import routers
from routes import (
    health_router,
    rooms_router,
    messages_router,
    websocket_router
)

# Create logger for chat-service
logger = SocketHubLogger("chat-service").get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting Chat Service...")
    try:
        # Initialize any required services here
        logger.info("✅ Chat Service initialized successfully")
    except Exception as e:
        logger.error(f"❌ Error initializing Chat Service: {e}")
        raise
    
    logger.info("✅ Chat Service started successfully")
    yield
    
    logger.info("🛑 Chat Service shutting down...")

app = FastAPI(
    title="Chat Service",
    description="Real-time chat service with rooms and messaging",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(rooms_router)
app.include_router(messages_router)
app.include_router(websocket_router)

@app.get("/")
async def root():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"message": "chat service is running", "status": "healthy"}
