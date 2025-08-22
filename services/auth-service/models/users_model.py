from pydantic import BaseModel
from datetime import datetime

class User (BaseModel):
    username: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime
