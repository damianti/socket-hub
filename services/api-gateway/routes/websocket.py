from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json

from models.websocket_models import MessageRequest, MessageResponse
from utils.connection_manager import ConnectionManager


manager = ConnectionManager()

router = APIRouter(
    prefix="/ws",
    tags=["websocker router"]
)

@router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    
    await websocket.accept()

    try:
        while True:
            raw_data = await websocket.receive_text()

            data = json.loads(raw_data)
            msg = MessageRequest(**data)
            if msg.type == "join_room":
                await manager.join_room(msg.room_id, msg.user_id)
                
            elif msg.type == "leave_room":
                await manager.leave_room(msg.room_id, msg.user_id)
            elif msg.type == "message":
                await manager.send_personal_message(msg.content, msg.user_id)

            await websocket.send_text(f"Echo: {data}")

    except WebSocketDisconnect:
        print (f"User {user_id} disconnected")
