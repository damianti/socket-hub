from fastapi import APIRouter, Depends, HTTPException
from db.repository import UserRepository
from models.users_model import UserCreate, UserResponse, LoginRequest, TokenResponse
from db.connection import get_db
from utils.jwt_utils import create_access_token
from middleware.auth_middleware import verify_token_middleware
import sys
import os

# Agregar el directorio shared al path para importar el logger
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from shared.logging import SocketHubLogger

# Crear logger para auth-router
logger = SocketHubLogger("auth-service").get_logger()

router = APIRouter(
    prefix="",
    tags=["auth"]
)

@router.post("/signup")
async def signup (request: UserCreate, db = Depends(get_db)) -> UserResponse:
    logger.info(f"📝 Registration attempt for user: {request.username}")
    try:
        repo = UserRepository(db)
        user = repo.create(request)
        logger.info(f"✅ User {request.username} registered successfully")
        return user
    except Exception as e:
        logger.error(f"❌ Error registering user {request.username}: {e}")
        raise

@router.post("/login")
async def login (request: LoginRequest, db = Depends(get_db)) -> TokenResponse:
    logger.info(f"🔐 Login attempt for user: {request.username}")
    try:
        repo = UserRepository(db)
        user = repo.verify_password(request.username, request.password)
        
        if not user:
            logger.warning(f"⚠️ Failed login for user: {request.username} - Invalid credentials")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create JWT token
        token_data = {"sub": user.username}
        access_token = create_access_token(data=token_data)
        
        logger.info(f"✅ Successful login for user: {request.username}")
        return TokenResponse(
            access_token=access_token,
            user=user
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error during login for user {request.username}: {e}")
        raise

@router.get("/me")
async def get_current_user(current_user = Depends(verify_token_middleware)):
    logger.info(f"👤 User {current_user.get('sub', 'unknown')} requesting profile information")
    return current_user

