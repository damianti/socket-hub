from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json
import sys
import os

from models.websocket_models import MessageRequest, MessageResponse
from utils.connection_manager import ConnectionManager

# Agregar el directorio shared al path para importar el logger
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from shared.logging import SocketHubLogger

# Crear logger para websocket
logger = SocketHubLogger("api-gateway").get_logger()


manager = ConnectionManager()

router = APIRouter(
    prefix="/ws",
    tags=["websocker router"]
)

@router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    logger.info(f"🔌 User {user_id} connecting via WebSocket")
    await websocket.accept()
    logger.info(f"✅ User {user_id} connected successfully")

    try:
        while True:
            raw_data = await websocket.receive_text()
            logger.debug(f"📨 Message received from {user_id}: {raw_data}")

            data = json.loads(raw_data)
            msg = MessageRequest(**data)
            
            if msg.type == "join_room":
                logger.info(f"🚪 User {user_id} joining room: {msg.room_id}")
                await manager.join_room(msg.room_id, msg.user_id)
                
            elif msg.type == "leave_room":
                logger.info(f"🚪 User {user_id} leaving room: {msg.room_id}")
                await manager.leave_room(msg.room_id, msg.user_id)
                
            elif msg.type == "message":
                logger.info(f"💬 User {user_id} sending message to room: {msg.room_id}")
                await manager.send_personal_message(msg.content, msg.user_id)

            await websocket.send_text(f"Echo: {data}")
            logger.debug(f"📤 Echo sent to {user_id}")

    except WebSocketDisconnect:
        logger.info(f"🔌 User {user_id} disconnected")
    except Exception as e:
        logger.error(f"❌ WebSocket error for user {user_id}: {e}")
        raise
