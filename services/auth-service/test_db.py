from db.connection import engine, Session
from db.models import User
from db.repository import UserRepository
from models.users_model import UserCreate
import os
from dotenv import load_dotenv

load_dotenv()

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    try:
        # Probar conexión
        with engine.connect() as connection:
            print("✅ Conexión a la base de datos exitosa")
            
        # Crear sesión
        session = Session()
        
        # Probar operaciones CRUD
        repo = UserRepository(session)
        
        # Crear usuario de prueba
        test_user = UserCreate(
            username="test_user",
            email="test@example.com",
            password="testpassword123"
        )
        
        # Intentar crear usuario
        try:
            user_response = repo.create(test_user)
            print(f"✅ Usuario creado exitosamente: {user_response.username}")
            
            # Probar login
            login_result = repo.verify_password("test_user", "testpassword123")
            if login_result:
                print(f"✅ Login exitoso: {login_result.username}")
            else:
                print("❌ Login falló")
                
        except ValueError as e:
            print(f"⚠️ Usuario ya existe: {e}")
            
        session.close()
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    test_database_connection()