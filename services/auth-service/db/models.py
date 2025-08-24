from sqlalchemy import Column, String, DateTime, UUID
from sqlalchemy.sql import func
from .connection import Base
import uuid


class User(Base):
    __tablename__ = "users"
    id = Column (UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column (String, unique=True, nullable=False)
    email = Column (String, unique=True, nullable=False)
    password_hash = Column (String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default= func.now())
    updated_at = Column(DateTime(timezone=True), onupdate= func.now())
