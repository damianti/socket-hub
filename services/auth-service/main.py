from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.health import router as health_router
from routes.auth_router import router as auth_router

import scripts.init_db as init_db

@asynccontextmanager
async def lifespan (app: FastAPI):
    init_db.init_database()
    yield

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
    return {"message": "auth is running", "status": "healthy"}

