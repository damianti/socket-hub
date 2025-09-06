from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    """Types of messages"""
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"

class MessageBase(BaseModel):
    """Base message model"""
    content: str
    message_type: MessageType = MessageType.TEXT
    room_id: str
    user_id: str

class MessageCreate(MessageBase):
    """Model for creating a new message"""
    pass

class MessageResponse(MessageBase):
    """Model for message responses"""
    id: str
    timestamp: datetime
    username: Optional[str] = None
    
    class Config:
        from_attributes = True

class MessageListResponse(BaseModel):
    """Model for listing messages"""
    messages: List[MessageResponse]
    total: int
    has_more: bool = False

class WebSocketMessage(BaseModel):
    """Model for WebSocket communication"""
    type: str  # "message", "join_room", "leave_room", "typing"
    content: Optional[str] = None
    room_id: str
    user_id: str
    timestamp: datetime
    username: Optional[str] = None

class TypingIndicator(BaseModel):
    """Model for typing indicators"""
    user_id: str
    username: str
    room_id: str
    is_typing: bool
