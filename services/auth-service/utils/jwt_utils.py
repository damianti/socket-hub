from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptoContext 
from config.settings import settings

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> dict | None:
    """
    Verifies and decodes a JWT token.
    
    Args:
        token (str): The JWT token to verify
        
    Returns:
        dict: The decoded token payload if valid
        
    Raises:
        JWTError: If token is invalid or has expired
    """
    try:
        decoded = jwt.decode(token, settings.JWT_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        if "sub" not in decoded:
            return None
        
        return decoded
    
    except JWTError:
        return None

