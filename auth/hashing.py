# Import necessary modules and packages
from passlib.context import CryptContext

# Create a CryptContext object with bcrypt as the encryption scheme and auto-deprecated for backward compatibility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    # Verify a plain password against a hashed password using the verify method of the CryptContext object
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    # Hash a password using the hash method of the CryptContext object
    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
