from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class User (BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: str
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str


