from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json
import sys
import os

# Add shared directory to path for logger import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from shared.logging import SocketHubLogger

# Import models
from models import WebSocketMessage, TypingIndicator

# Create logger for websocket routes
logger = SocketHubLogger("chat-service").get_logger()

router = APIRouter(
    prefix="/ws",
    tags=["websocket"]
)

# Mock connection manager - will be replaced with real service later
class MockConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.room_connections: Dict[str, set] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"User {user_id} connected to chat service")
    
    async def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        # Remove from all rooms
        for room_id in list(self.room_connections.keys()):
            if user_id in self.room_connections[room_id]:
                self.room_connections[room_id].remove(user_id)
        
        logger.info(f"User {user_id} disconnected from chat service")
    
    async def join_room(self, room_id: str, user_id: str):
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
            logger.info(f"New room created: {room_id}")
        
        self.room_connections[room_id].add(user_id)
        logger.info(f"User {user_id} joined room {room_id}")
    
    async def leave_room(self, room_id: str, user_id: str):
        if room_id in self.room_connections and user_id in self.room_connections[room_id]:
            self.room_connections[room_id].remove(user_id)
            logger.info(f"User {user_id} left room {room_id}")
    
    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)
            logger.debug(f"Personal message sent to {user_id}")
    
    async def broadcast_to_room(self, message: str, room_id: str, exclude_user: str = None):
        if room_id in self.room_connections:
            users_in_room = len(self.room_connections[room_id])
            logger.info(f"Broadcasting to room {room_id} ({users_in_room} users)")
            
            for user_id in self.room_connections[room_id]:
                if user_id != exclude_user:
                    await self.send_personal_message(message, user_id)

# Global connection manager instance
manager = MockConnectionManager()

@router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time chat"""
    logger.info(f"User {user_id} connecting via WebSocket")
    
    try:
        await manager.connect(websocket, user_id)
        logger.info(f"User {user_id} connected successfully")
        
        while True:
            # Receive message from client
            raw_data = await websocket.receive_text()
            logger.debug(f"Message received from {user_id}: {raw_data}")
            
            try:
                # Parse the message
                data = json.loads(raw_data)
                ws_message = WebSocketMessage(**data)
                
                # Handle different message types
                if ws_message.type == "join_room":
                    logger.info(f"User {user_id} joining room: {ws_message.room_id}")
                    await manager.join_room(ws_message.room_id, user_id)
                    
                    # Send confirmation
                    response = {
                        "type": "room_joined",
                        "room_id": ws_message.room_id,
                        "user_id": user_id,
                        "message": f"Joined room {ws_message.room_id}"
                    }
                    await manager.send_personal_message(json.dumps(response), user_id)
                
                elif ws_message.type == "leave_room":
                    logger.info(f"User {user_id} leaving room: {ws_message.room_id}")
                    await manager.leave_room(ws_message.room_id, user_id)
                    
                    # Send confirmation
                    response = {
                        "type": "room_left",
                        "room_id": ws_message.room_id,
                        "user_id": user_id,
                        "message": f"Left room {ws_message.room_id}"
                    }
                    await manager.send_personal_message(json.dumps(response), user_id)
                
                elif ws_message.type == "message":
                    logger.info(f"User {user_id} sending message to room: {ws_message.room_id}")
                    
                    # Broadcast message to all users in room
                    message_response = {
                        "type": "message",
                        "content": ws_message.content,
                        "room_id": ws_message.room_id,
                        "user_id": user_id,
                        "username": "current_user",  # Will be replaced with real username
                        "timestamp": ws_message.timestamp
                    }
                    
                    await manager.broadcast_to_room(
                        json.dumps(message_response),
                        ws_message.room_id,
                        exclude_user=user_id
                    )
                    
                    # Send confirmation to sender
                    confirmation = {
                        "type": "message_sent",
                        "message_id": f"msg-{len(manager.active_connections)}",  # Mock ID
                        "room_id": ws_message.room_id
                    }
                    await manager.send_personal_message(json.dumps(confirmation), user_id)
                
                elif ws_message.type == "typing":
                    logger.debug(f"User {user_id} typing in room: {ws_message.room_id}")
                    
                    # Broadcast typing indicator to other users in room
                    typing_response = {
                        "type": "typing",
                        "user_id": user_id,
                        "username": "current_user",  # Will be replaced with real username
                        "room_id": ws_message.room_id,
                        "is_typing": True
                    }
                    
                    await manager.broadcast_to_room(
                        json.dumps(typing_response),
                        ws_message.room_id,
                        exclude_user=user_id
                    )
                
                else:
                    logger.warning(f"Unknown message type from {user_id}: {ws_message.type}")
                    error_response = {
                        "type": "error",
                        "message": f"Unknown message type: {ws_message.type}"
                    }
                    await manager.send_personal_message(json.dumps(error_response), user_id)
            
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON from {user_id}: {e}")
                error_response = {
                    "type": "error",
                    "message": "Invalid JSON format"
                }
                await manager.send_personal_message(json.dumps(error_response), user_id)
            
            except Exception as e:
                logger.error(f"Error processing message from {user_id}: {e}")
                error_response = {
                    "type": "error",
                    "message": "Internal server error"
                }
                await manager.send_personal_message(json.dumps(error_response), user_id)
    
    except WebSocketDisconnect:
        logger.info(f"User {user_id} disconnected")
        await manager.disconnect(user_id)
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        await manager.disconnect(user_id)
        raise
