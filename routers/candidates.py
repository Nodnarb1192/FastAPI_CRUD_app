# Import the necessary modules and packages
from fastapi import APIRouter,HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse
from db.engine import db
from schemas.candidates import Candidates,CandidateObject, VerifyUser
from auth.oauth2 import get_current_user
from schemas.user import UserModel
from auth.hashing import Hasher
import pandas as pd
from starlette.responses import FileResponse, StreamingResponse
import csv
from bson import ObjectId

# Create a new API router for the Candidate endpoints
candidate_router = APIRouter(tags=["Candidate"])

# Define the /candidate endpoint for getting all candidates for a user
@candidate_router.get("/candidate")
async def all_candidate(currentuser: UserModel = Depends(get_current_user)):
    user = db.users.find_one({"email":currentuser.email})
    user = VerifyUser(**user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user is not valid")
    candidates = []
    # Get all candidates for the current user from the database
    for i in db.candidates.find({"user_id":user.id}):
        candidates.append(Candidates(**i))
    return candidates

# Define the /candidate endpoint for creating a new candidate
@candidate_router.post("/candidate/")
async def create_candidates(request: CandidateObject,currentuser: UserModel = Depends(get_current_user)):
    user = db.users.find_one({"email":currentuser.email})
    user = VerifyUser(**user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user is not valid")
    # Check if a candidate with the same email already exists in the database
    candidate = db.candidates.find_one({"email":request.email})
    if candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Aleady Register!")
    
    # Hash the UUID and add the user ID to the request data
    insert_data = request.dict(exclude_unset=True)
    insert_data['UUID'] = Hasher.get_password_hash(insert_data['UUID'])
    insert_data['user_id'] = user.id

     # Insert the new candidate into the database
    db.candidates.insert_one(dict(insert_data))
    return JSONResponse(content={}, status_code=201)

# Define the /candidate/{id} endpoint for updating an existing candidate
@candidate_router.put("/candidate/{id}")
async def update_candidate(id: str,request: CandidateObject,currentuser: UserModel = Depends(get_current_user)):
    user = db.users.find_one({"email":currentuser.email})
    user = VerifyUser(**user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user is not valid")
    # Check if a candidate with the given ID exists in the database
    try:
        candidate = db.candidates.find_one({"_id":ObjectId(f"{id}")})
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Candidate Found!")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Candidate id is not valid")
    # Check if a candidate with the same email already exists in the database
    if candidate['email'] != request.email:
        candidate_email = db.candidates.find_one({"email":request.email})
        if candidate_email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Email Aleady Register!")

    # Check if the current user owns the candidate record
    if user.id != candidate['user_id']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Method Not Allowed!")
    # Hash the UUID and update the candidate data in the database
    candidate_data = request.dict(exclude_unset=True)
    candidate_data['UUID'] = Hasher.get_password_hash(candidate_data['UUID'])
    candidate = db.candidates.find_one_and_update(
        {"_id":ObjectId(f"{id}")},
        {'$set':candidate_data}
    )
    return JSONResponse(content={}, status_code=200)

# Define the /candidate/{id} endpoint for getting a single candidate by ID
@candidate_router.get("/candidate/{id}")
async def get_one_candidate(id: str,currentuser: UserModel = Depends(get_current_user)):
    user = db.users.find_one({"email":currentuser.email})
    user = VerifyUser(**user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user is not valid")
    # Check if a candidate with the given ID exists in the database
    try:
        candidate = db.candidates.find_one({"_id":ObjectId(f"{id}")})
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Candidate Found!")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Candidate id is not valid")
    # Check if the current user owns the candidate record
    if user.id != candidate['user_id']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Method Not Allowed!")
    # Return the candidate data
    candidate = Candidates(**candidate)
    return candidate 

# Define the /candidate/{id} endpoint for deleting a candidate by ID
@candidate_router.delete("/candidate/{id}")
async def delete_candidate(id: str,currentuser: UserModel = Depends(get_current_user)):
    user = db.users.find_one({"email":currentuser.email})
    user = VerifyUser(**user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user is not valid")
    # Check if a candidate with the given ID exists in the database
    try:
        candidate = db.candidates.find_one({"_id":ObjectId(f"{id}")})
        if not candidate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Candidate Found!")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Candidate id is not valid")
    # Check if the current user owns the candidate record
    if user.id != candidate['user_id']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Method Not Allowed!")
    # Delete the candidate from the database
    db.candidates.delete_one({"_id":ObjectId(f"{id}")})
    return JSONResponse(content={}, status_code=200)

# Define the /all-candidates endpoint for getting all candidates with optional query parameters
@candidate_router.get("/all-candidates")
async def all_candidate(request:Request, currentuser: UserModel = Depends(get_current_user)):
    params = request.query_params._dict
    candidates = list()
    # Get all candidates from the database that match the given query parameters
    for i in db.candidates.find(params):
        candidates.append(Candidates(**i))

    return candidates

# Define the /generate-report endpoint for generating a CSV report of all candidates
@candidate_router.get("/generate-report")
async def generate_report(currentuser: UserModel = Depends(get_current_user)):
    # define the CSV header
    fieldnames = [
        'first_name', 
        'last_name', 
        'email', 
        'uuid', 
        'career_level', 
        'job_major', 
        'years_of_experience', 
        'degree_type', 
        'skills', 
        'nationality', 
        'city', 
        'salary', 
        'gender'
    ]

    # create a generator that yields CSV rows for each candidate
    def generate_csv():
        # write the CSV header row
        yield ','.join(fieldnames) + '\n'

        # iterate over all candidates in the database
        for candidate in db.candidates.find():
            # convert the candidate to a dictionary
            candidate_dict = dict(candidate)

            # format the skills list as a comma-separated string
            candidate_dict['skills'] = '"' + ', '.join(candidate_dict['skills']) + '"'

            # write a row for the candidate to the CSV
            row = [str(candidate_dict.get(field, '')) for field in fieldnames]
            yield ','.join(row) + '\n'

    # create a StreamingResponse that streams the generated CSV
    return StreamingResponse(generate_csv(), headers={
        'Content-Disposition': 'attachment; filename="candidates.csv"',
        'Content-Type': 'text/csv',
    })
