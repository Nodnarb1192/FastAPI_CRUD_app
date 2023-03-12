# Import the necessary modules and packages
import time
import os
from jose import JWTError, jwt
from schemas.user import TokenData

def create_access_token(data: dict):
    # Create payload for the access token
    payload = {
        "userID": data,
        "expiry": time.time() + 20000
    }
    
    # Encode the payload with the secret key and algorithm specified in environment variables
    encoded_jwt = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

def validUser(token: str, credentials_exception):
    try:
        # Decode the token using the secret key and algorithm specified in environment variables
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        email: str = payload.get("userID")

        # Raise an exception if the token does not contain a user ID
        if email is None:
            raise credentials_exception
        
        # Create a TokenData object with the user ID from the token
        token_data = TokenData(email=email)
        return token_data
    
    # Raise an exception if the token is invalid
    except JWTError:
        raise credentials_exception
    