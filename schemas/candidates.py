# Import the necessary modules and packages
from pydantic import BaseModel,EmailStr,validator,Field
from typing import Optional, List
from bson import ObjectId
from schemas.user import User

# This class extends the ObjectId class from the bson library to be used by the Candidate Management app.
class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

# This class defines the CandidateObject schema used by the Candidate Management app.
class CandidateObject(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    UUID: str
    career_level: str
    job_major: str
    years_of_experience: int
    degree_type: str
    skills: List[str]
    nationality: str
    city: str
    salary: int
    gender: str
    
    # This validator ensures that the gender field is one of 'Male', 'Female', or 'Not Specific'.
    @validator('gender')
    def gender_match(cls,v):
        if not v in ['Male', 'Female', 'Not Specific']:
            raise ValueError("skills must be in ['Male', 'Female', 'Not Specific']")
        return v

# This class extends the CandidateObject schema to include an ObjectId field.
class Candidates(CandidateObject):
    id: Optional[PyObjectId] = Field(alias='_id') 
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

# This class extends the User schema from the schemas.user module to include an ObjectId field.
class VerifyUser(User):
    id: Optional[PyObjectId] = Field(alias='_id') 
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        