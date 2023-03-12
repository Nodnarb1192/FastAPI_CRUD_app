# Import the necessary modules and packages
from pydantic import BaseModel, EmailStr
from typing import Union

# This class defines the User model used by the Candidate Management app.
class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    uuid: str
    password: str

# This class defines the TokenData model used by the Candidate Management app.
class TokenData(BaseModel):
    email: Union[str, None] = None

# This class defines the LoginUser model used by the Candidate Management app.
class LoginUser(BaseModel):
    username: EmailStr
    password: str

# This class defines the UserModel used by the Candidate Management app.
class UserModel(BaseModel):
    name : str
    email : str
    password : str
    