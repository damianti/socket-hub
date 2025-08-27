from pydantic_settings import BaseSettings
from pydantic import  validator
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    PORT: int
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int

    @validator('JWT_KEY')
    def validate_secret_key (cls, v):
        if len(v) < 32:
            raise ValueError('JWT_KEY must be at least 32 characters')
        return v

class Config:
    env_file = ".env"


settings = Settings()