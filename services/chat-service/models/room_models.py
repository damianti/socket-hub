from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RoomBase(BaseModel):
    """Base room model with common fields"""
    name: str
    description: Optional[str] = None
    is_private: bool = False

class RoomCreate(RoomBase):
    """Model for creating a new room"""
    pass

class RoomResponse(RoomBase):
    """Model for room responses"""
    id: str
    created_at: datetime
    user_count: int = 0
    created_by: str
    
    class Config:
        from_attributes = True

class RoomListResponse(BaseModel):
    """Model for listing rooms"""
    rooms: List[RoomResponse]
    total: int

class RoomJoinRequest(BaseModel):
    """Model for joining a room"""
    room_id: str
    user_id: str

class RoomLeaveRequest(BaseModel):
    """Model for leaving a room"""
    room_id: str
    user_id: str
