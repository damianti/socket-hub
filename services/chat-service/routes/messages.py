from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import sys
import os

# Add shared directory to path for logger import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from shared.logging import SocketHubLogger

# Import models
from models import (
    MessageCreate,
    MessageResponse,
    MessageListResponse,
    MessageType
)

# Create logger for message routes
logger = SocketHubLogger("chat-service").get_logger()

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

# Mock data for now - will be replaced with real service later
mock_messages = [
    {
        "id": "msg-1",
        "content": "Hello everyone!",
        "message_type": "text",
        "room_id": "room-1",
        "user_id": "user-1",
        "timestamp": "2024-01-01T00:00:00Z",
        "username": "john_doe"
    },
    {
        "id": "msg-2",
        "content": "How is everyone doing?",
        "message_type": "text", 
        "room_id": "room-1",
        "user_id": "user-2",
        "timestamp": "2024-01-01T00:01:00Z",
        "username": "jane_smith"
    }
]

@router.get("/room/{room_id}", response_model=MessageListResponse)
async def get_room_messages(
    room_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get messages from a specific room"""
    logger.info(f"Getting messages for room {room_id} (limit: {limit}, offset: {offset})")
    try:
        # Filter messages by room_id
        room_messages = [msg for msg in mock_messages if msg["room_id"] == room_id]
        
        # Apply pagination
        total = len(room_messages)
        messages = room_messages[offset:offset + limit]
        has_more = offset + limit < total
        
        # Convert to response models
        message_responses = [MessageResponse(**msg) for msg in messages]
        
        logger.info(f"Retrieved {len(message_responses)} messages for room {room_id}")
        return MessageListResponse(
            messages=message_responses,
            total=total,
            has_more=has_more
        )
    except Exception as e:
        logger.error(f"Error getting messages for room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=MessageResponse)
async def create_message(message_data: MessageCreate):
    """Create a new message"""
    logger.info(f"Creating new message in room {message_data.room_id} by user {message_data.user_id}")
    try:
        # Mock message creation - will be replaced with real service
        new_message = {
            "id": f"msg-{len(mock_messages) + 1}",
            "content": message_data.content,
            "message_type": message_data.message_type.value,
            "room_id": message_data.room_id,
            "user_id": message_data.user_id,
            "timestamp": "2024-01-01T00:00:00Z",
            "username": "current_user"  # Will be replaced with real username
        }
        mock_messages.append(new_message)
        
        logger.info(f"Message created successfully: {new_message['id']}")
        return MessageResponse(**new_message)
    except Exception as e:
        logger.error(f"Error creating message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(message_id: str):
    """Get a specific message by ID"""
    logger.info(f"Getting message: {message_id}")
    try:
        message = next((msg for msg in mock_messages if msg["id"] == message_id), None)
        if not message:
            logger.warning(f"Message not found: {message_id}")
            raise HTTPException(status_code=404, detail="Message not found")
        
        return MessageResponse(**message)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting message {message_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{message_id}")
async def delete_message(message_id: str):
    """Delete a message (soft delete)"""
    logger.info(f"Deleting message: {message_id}")
    try:
        message = next((msg for msg in mock_messages if msg["id"] == message_id), None)
        if not message:
            logger.warning(f"Message not found: {message_id}")
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Mock deletion - will be replaced with real service
        # In real implementation, you would mark as deleted or remove from database
        mock_messages.remove(message)
        
        logger.info(f"Message deleted successfully: {message_id}")
        return {"message": "Message deleted successfully", "message_id": message_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting message {message_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/user/{user_id}", response_model=MessageListResponse)
async def get_user_messages(
    user_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Get messages from a specific user"""
    logger.info(f"Getting messages from user {user_id} (limit: {limit}, offset: {offset})")
    try:
        # Filter messages by user_id
        user_messages = [msg for msg in mock_messages if msg["user_id"] == user_id]
        
        # Apply pagination
        total = len(user_messages)
        messages = user_messages[offset:offset + limit]
        has_more = offset + limit < total
        
        # Convert to response models
        message_responses = [MessageResponse(**msg) for msg in messages]
        
        logger.info(f"Retrieved {len(message_responses)} messages from user {user_id}")
        return MessageListResponse(
            messages=message_responses,
            total=total,
            has_more=has_more
        )
    except Exception as e:
        logger.error(f"Error getting messages from user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
