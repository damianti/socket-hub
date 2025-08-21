from pydantic import BaseModel
from datetime import datetime

class MessageRequest (BaseModel):
    type: str
    content: str
    room_id: str
    user_id: str
    timestamp: datetime

class MessageResponse (BaseModel):
    type: str
    content: str
    room_id: str
    user_id: str
    timestamp: datetime
