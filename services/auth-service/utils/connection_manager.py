from fastapi import WebSocket



class ConnectionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.active_connections = {}
            cls._instance.room_connections = {}
        return cls._instance


    async def connect (self, websocket: WebSocket, user_id: str) -> None:
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"User {user_id} connected")
    
    async def disconnect (self, user_id: str) -> None:
        del self.active_connections[user_id]
        
        for room_id in list(self.room_connections.keys()):
            if user_id in self.room_connections[room_id]:
                self.room_connections[room_id].remove(user_id)
        print(f"User {user_id} disconnected")

    async def join_room (self, room_id: str, user_id: str) -> None:
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
        
        self.room_connections[room_id].add(user_id)
        print(f"User {user_id} joined room {room_id}")
            
        
    async def leave_room (self, room_id: str, user_id: str) -> None:
        if room_id in self.room_connections and user_id in self.room_connections[room_id]:
            self.room_connections[room_id].remove(user_id)
        print(f"User {user_id} left room {room_id}")

    async def send_personal_message(self, message:str, user_id:str) -> None:
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

    async def broadcast_to_room(self, message: str, room_id: str, exclude_user: str):
        if room_id in self.room_connections:
            for user_id in self.room_connections[room_id]:
                if user_id != exclude_user:
                    await self.send_personal_message(message, user_id)