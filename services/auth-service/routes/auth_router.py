from fastapi import APIRouter, Depends
from db.repository import UserRepository
from models.users_model import UserCreate, UserResponse
from db.connection import get_db


router = APIRouter(
    prefix="",
    tags=["auth"]
)

@router.post("/signup")
async def signup (request: UserCreate, db = Depends(get_db)) -> UserResponse:
    repo = UserRepository(db)
    return repo.create(request)


@router.post("/login")
async def login (username: str, password: str, db = Depends(get_db)) -> UserResponse | None:
    repo = UserRepository(db)
    return repo.verify_password(username, password)

