from argon2 import PasswordHasher
from typing import Optional

class PasswordHasherUtil:
    """
    Singleton utility class for password hashing to ensure consistency
    across all repository instances.
    """
    _instance: Optional['PasswordHasherUtil'] = None
    _hasher: Optional[PasswordHasher] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PasswordHasherUtil, cls).__new__(cls)
            # Initialize with consistent parameters
            cls._hasher = PasswordHasher(
                time_cost=3,      # Number of iterations
                memory_cost=65536, # Memory usage in KiB
                parallelism=4,    # Number of parallel threads
                hash_len=32       # Length of the hash
            )
        return cls._instance
    
    def hash(self, password: str) -> str:
        """Hash a password with consistent parameters"""
        return self._hasher.hash(password)
    
    def verify(self, hash: str, password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return self._hasher.verify(hash, password)
        except Exception:
            return False

# Global instance
password_hasher = PasswordHasherUtil()
