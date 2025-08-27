from fastapi import APIRouter, Depends, HTTPException
from db.repository import UserRepository
from models.users_model import UserCreate, UserResponse, LoginRequest, TokenResponse
from db.connection import get_db
from utils.jwt_utils import create_access_token
from middleware.auth_middleware import verify_token_middleware

router = APIRouter(
    prefix="",
    tags=["auth"]
)

@router.post("/signup")
async def signup (request: UserCreate, db = Depends(get_db)) -> UserResponse:
    repo = UserRepository(db)
    return repo.create(request)

@router.post("/login")
async def login (request: LoginRequest, db = Depends(get_db)) -> TokenResponse:
    repo = UserRepository(db)
    user = repo.verify_password(request.username, request.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT token
    token_data = {"sub": user.username}
    access_token = create_access_token(data=token_data)
    
    return TokenResponse(
        access_token=access_token,
        user=user
    )

@router.get("/me")
async def get_current_user(current_user = Depends(verify_token_middleware)):
    return current_user

