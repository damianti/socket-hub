from fastapi import APIRouter, HTTPException, Depends
from typing import List
import sys
import os

# Add shared directory to path for logger import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from shared.logging import SocketHubLogger

# Import models
from models import (
    RoomCreate,
    RoomResponse,
    RoomListResponse,
    RoomJoinRequest,
    RoomLeaveRequest,
    RoomUserListResponse
)

# Create logger for room routes
logger = SocketHubLogger("chat-service").get_logger()

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"]
)

# Mock data for now - will be replaced with real service later
mock_rooms = [
    {
        "id": "room-1",
        "name": "General",
        "description": "General discussion room",
        "is_private": False,
        "created_at": "2024-01-01T00:00:00Z",
        "user_count": 5,
        "created_by": "admin"
    },
    {
        "id": "room-2", 
        "name": "Tech Talk",
        "description": "Technology discussions",
        "is_private": False,
        "created_at": "2024-01-01T00:00:00Z",
        "user_count": 3,
        "created_by": "admin"
    }
]

@router.get("/", response_model=RoomListResponse)
async def list_rooms():
    """List all available rooms"""
    logger.info("Listing all rooms")
    try:
        rooms = [RoomResponse(**room) for room in mock_rooms]
        return RoomListResponse(rooms=rooms, total=len(rooms))
    except Exception as e:
        logger.error(f"Error listing rooms: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=RoomResponse)
async def create_room(room_data: RoomCreate):
    """Create a new room"""
    logger.info(f"Creating new room: {room_data.name}")
    try:
        # Mock room creation - will be replaced with real service
        new_room = {
            "id": f"room-{len(mock_rooms) + 1}",
            "name": room_data.name,
            "description": room_data.description,
            "is_private": room_data.is_private,
            "created_at": "2024-01-01T00:00:00Z",
            "user_count": 0,
            "created_by": "current_user"  # Will be replaced with real user
        }
        mock_rooms.append(new_room)
        
        logger.info(f"Room created successfully: {new_room['id']}")
        return RoomResponse(**new_room)
    except Exception as e:
        logger.error(f"Error creating room: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: str):
    """Get room details by ID"""
    logger.info(f"Getting room details: {room_id}")
    try:
        room = next((room for room in mock_rooms if room["id"] == room_id), None)
        if not room:
            logger.warning(f"Room not found: {room_id}")
            raise HTTPException(status_code=404, detail="Room not found")
        
        return RoomResponse(**room)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{room_id}/join")
async def join_room(room_id: str, join_request: RoomJoinRequest):
    """Join a room"""
    logger.info(f"User {join_request.user_id} joining room {room_id}")
    try:
        # Mock join logic - will be replaced with real service
        room = next((room for room in mock_rooms if room["id"] == room_id), None)
        if not room:
            logger.warning(f"Room not found: {room_id}")
            raise HTTPException(status_code=404, detail="Room not found")
        
        # Increment user count
        room["user_count"] += 1
        
        logger.info(f"User {join_request.user_id} joined room {room_id} successfully")
        return {"message": "Successfully joined room", "room_id": room_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error joining room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{room_id}/leave")
async def leave_room(room_id: str, leave_request: RoomLeaveRequest):
    """Leave a room"""
    logger.info(f"User {leave_request.user_id} leaving room {room_id}")
    try:
        # Mock leave logic - will be replaced with real service
        room = next((room for room in mock_rooms if room["id"] == room_id), None)
        if not room:
            logger.warning(f"Room not found: {room_id}")
            raise HTTPException(status_code=404, detail="Room not found")
        
        # Decrement user count
        if room["user_count"] > 0:
            room["user_count"] -= 1
        
        logger.info(f"User {leave_request.user_id} left room {room_id} successfully")
        return {"message": "Successfully left room", "room_id": room_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error leaving room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{room_id}/users", response_model=RoomUserListResponse)
async def get_room_users(room_id: str):
    """Get users in a room"""
    logger.info(f"Getting users in room: {room_id}")
    try:
        # Mock user data - will be replaced with real service
        mock_users = [
            {
                "user_id": "user-1",
                "username": "john_doe",
                "joined_at": "2024-01-01T00:00:00Z",
                "is_active": True
            },
            {
                "user_id": "user-2", 
                "username": "jane_smith",
                "joined_at": "2024-01-01T00:00:00Z",
                "is_active": True
            }
        ]
        
        return RoomUserListResponse(users=mock_users, total=len(mock_users))
    except Exception as e:
        logger.error(f"Error getting users for room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
