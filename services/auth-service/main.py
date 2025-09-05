from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.health import router as health_router
from routes.auth_router import router as auth_router

import scripts.init_db as init_db
import sys
import os

# Agregar el directorio shared al path para importar el logger
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.logging import SocketHubLogger

# Crear logger para auth-service
logger = SocketHubLogger("auth-service").get_logger()

@asynccontextmanager
async def lifespan (app: FastAPI):
    logger.info("🚀 Starting Auth Service...")
    try:
        init_db.init_database()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Error initializing database: {e}")
        raise
    
    logger.info("✅ Auth Service started successfully")
    yield
    
    logger.info("🛑 Auth Service shutting down...")

app = FastAPI(
    title="authentication service",
    description="this service authenticates users",
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

app.include_router(health_router)
app.include_router(auth_router, prefix="/auth")


@app.get("/")
async def root():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"message": "auth is running", "status": "healthy"}

