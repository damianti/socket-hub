from fastapi import WebSocket
import sys
import os

# Agregar el directorio shared al path para importar el logger
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from shared.logging import SocketHubLogger



class ConnectionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.active_connections = {}
            cls._instance.room_connections = {}
            cls._instance.logger = SocketHubLogger("api-gateway").get_logger()
        return cls._instance


    async def connect (self, websocket: WebSocket, user_id: str) -> None:
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.logger.info(f"🔌 User {user_id} connected to ConnectionManager")
    
    async def disconnect (self, user_id: str) -> None:
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        for room_id in list(self.room_connections.keys()):
            if user_id in self.room_connections[room_id]:
                self.room_connections[room_id].remove(user_id)
        self.logger.info(f"🔌 User {user_id} disconnected from ConnectionManager")

    async def join_room (self, room_id: str, user_id: str) -> None:
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
            self.logger.info(f"🏠 New room created: {room_id}")
        
        self.room_connections[room_id].add(user_id)
        self.logger.info(f"🚪 User {user_id} joined room {room_id}")
            
        
    async def leave_room (self, room_id: str, user_id: str) -> None:
        if room_id in self.room_connections and user_id in self.room_connections[room_id]:
            self.room_connections[room_id].remove(user_id)
            self.logger.info(f"🚪 User {user_id} left room {room_id}")
        else:
            self.logger.warning(f"⚠️ User {user_id} tried to leave room {room_id} but was not in it")

    async def send_personal_message(self, message:str, user_id:str) -> None:
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)
            self.logger.debug(f"📤 Personal message sent to {user_id}")
        else:
            self.logger.warning(f"⚠️ Could not send message to {user_id} - not connected")

    async def broadcast_to_room(self, message: str, room_id: str, exclude_user: str):
        if room_id in self.room_connections:
            users_in_room = len(self.room_connections[room_id])
            self.logger.info(f"📢 Broadcasting to room {room_id} ({users_in_room} users)")
            for user_id in self.room_connections[room_id]:
                if user_id != exclude_user:
                    await self.send_personal_message(message, user_id)
        else:
            self.logger.warning(f"⚠️ Could not broadcast to room {room_id} - room does not exist")