from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserInfo(BaseModel):
    """Basic user information for chat"""
    user_id: str
    username: str
    is_online: bool = False
    last_seen: Optional[datetime] = None

class UserPresence(BaseModel):
    """User presence information"""
    user_id: str
    username: str
    status: str = "online"  # online, away, busy, offline
    current_room: Optional[str] = None

class RoomUser(BaseModel):
    """User information within a room context"""
    user_id: str
    username: str
    joined_at: datetime
    is_active: bool = True

class UserListResponse(BaseModel):
    """Model for listing users"""
    users: List[UserInfo]
    total: int

class RoomUserListResponse(BaseModel):
    """Model for listing users in a room"""
    users: List[RoomUser]
    total: int
