from db.connection import engine, Session
from db.models import User
from db.repository import UserRepository
from models.users_model import UserCreate
import os
from dotenv import load_dotenv

load_dotenv()


def test_database_connection():
    """Tests the database connection"""
    try:
        # Test connection
        with engine.connect() as connection:
            print("✅ Database connection successful")
            
        # Create session
        session = Session()
        
        # Test CRUD operations
        repo = UserRepository(session)
        
        # Create test user
        test_user = UserCreate(
            username="test_user",
            email="test@example.com",
            password="testpassword123"
        )
        
        # Try to create user
        try:
            user_response = repo.create(test_user)
            print(f"✅ User created successfully: {user_response.username}")
            
            # Test login
            login_result = repo.verify_password("test_user", "testpassword123")
            if login_result:
                print(f"✅ Login successful: {login_result.username}")
            else:
                print("❌ Login failed")
                
        except ValueError as e:
            print(f"⚠️ User already exists: {e}")
            
        session.close()
        
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_database_connection()