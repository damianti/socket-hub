from pydantic import BaseModel

class SignupRequest(BaseModel):
    username:str
    email:str
    password:str

class LoginRequest(BaseModel):
    username:str
    email:str   
    password:str

class UserResponse(BaseModel):
    username:str
    email:str
    