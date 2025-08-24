import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/socket_hub")
    ECHO_SQL = os.getenv("ECHO_SQL", "False").lower() == "true"
