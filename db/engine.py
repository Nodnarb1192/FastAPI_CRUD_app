# Import the necessary modules and packages
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a MongoDB client and connect to the local test database
client = MongoClient("mongodb://localhost:27017/test")

# Get the database with the name specified in the DATABASE_NAME environment variable
db = client[os.getenv('DATABASE_NAME')]

# Get the 'users' collection from the database
users_collection = db['users']