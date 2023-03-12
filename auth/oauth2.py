# Import the necessary modules and packages
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,Depends,status
from . import token

# Create an OAuth2PasswordBearer instance with the token URL for login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login/")


async def get_current_user(data: str = Depends(oauth2_scheme)):
    # Create an exception to be raised if the credentials cannot be validated
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Call the validUser function from token.py to decode and validate the token
    return token.validUser(data,credentials_exception)
