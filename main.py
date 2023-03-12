# Import the necessary modules and packages
from fastapi import FastAPI
from routers.user import user_router
from routers.candidates import candidate_router
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a new instance of the FastAPI class
app = FastAPI()

# Include the user_router and candidate_router routers in the app
app.include_router(user_router)
app.include_router(candidate_router)