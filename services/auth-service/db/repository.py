from abc import ABC, abstractmethod
from models.users_model import UserCreate, UserResponse
from db.models import User
from utils.password_hasher import password_hasher


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id): pass

    @abstractmethod
    def create(self, SignupRequest): pass

class UserRepository(IUserRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, user_id):
        return self.session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, user_email):
        return self.session.query(User).filter(User.email == user_email).first()

    def get_user_by_username(self, user_username):
        return self.session.query(User).filter(User.username == user_username).first()

    def create(self, request: UserCreate) -> UserResponse:
        if self.get_user_by_username(request.username):
            raise ValueError("Username already exists")
        if self.get_user_by_email(request.email):
            raise ValueError("email already exists")
            
        new_user = User(username=request.username, email=request.email, password_hash=password_hasher.hash(request.password))
        self.session.add(new_user)
        self.session.commit()

        return UserResponse(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            created_at=new_user.created_at
        )

    def verify_password(self, username:str, password:str) -> UserResponse | None:
        user = self.get_user_by_username(username)
        if user and password_hasher.verify(user.password_hash, password):
            return UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                created_at=user.created_at
            )
        return None