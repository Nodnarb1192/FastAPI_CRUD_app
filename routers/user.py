# Import the necessary modules and packages
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from schemas.user import User
from db.engine import db
from auth.hashing import Hasher
from auth.token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

# Create a new API router for the User endpoints
user_router = APIRouter(tags=["User"])

# Define the /user/signup/ endpoint for creating a new user account
@user_router.post("/user/signup/")
def user_signup(request: User):
    # Check if the user already exists in the database
    user = db.users.find_one({"email":request.email})
    if not user:
        # If the user doesn't exist, create a new account
        data = {
            "first_name":request.first_name,
            "last_name": request.last_name,
            "email": request.email,
            "uuid": request.uuid,
            "password": Hasher.get_password_hash(request.password)
        }
        db.users.insert_one(data)
        access_token = create_access_token(request.email)
        return JSONResponse(content={"access_token":access_token}, status_code=201)
    else:
        # If the user already exists, raise an HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"User with same email is already register")

# Define the /user/login/ endpoint for user authentication
@user_router.post("/user/login/")
async def login_user(request: OAuth2PasswordRequestForm = Depends()):
    # Check if the user exists in the database
    user = db.users.find_one({"email":request.username})

    if not user:
        # If the user doesn't exist, raise an HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user is not valid")
    
    elif not Hasher.verify_password(request.password,user['password']):
        # If the password is incorrect, raise an HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"User or Password is not valid")
    
    # If the user and password are valid, create an access token and return it
    access_token = create_access_token(request.username)
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, status_code=200)