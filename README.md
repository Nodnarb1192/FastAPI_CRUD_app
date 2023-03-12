
# Candidate Management API

This API allows you to manage candidates by adding, updating, deleting, and retrieving candidate data. It also allows generating a CSV report of all candidates.




## Technologies Used

- **FastAPI:** FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

- **MongoDB:** MongoDB is a general purpose, document-based, distributed database built for modern application developers and for the cloud era.

- **Pydantic:** Pydantic is a data validation and settings management library using Python type annotations.

- **Passlib:** Passlib is a password hashing library for Python 2 & 3, which provides cross-platform implementations of over 30 password hashing algorithms.

- **JWT:** JSON Web Tokens are an open, industry standard RFC 7519 method for representing claims securely between two parties.




## Setup

1. Clone this repository

```bash
  $ git clone https://github.com/Nodnarb1192/FastAPI_CRUD_app.git
  $ cd FastAPI_CRUD_app
```

2. Create a virtual environment and activate it:

``` bash
$ python -m venv venv
$ source venv/bin/activate (for Unix systems)
$ venv\Scripts\activate (for Windows systems)
```

3. Install the dependencies:

``` bash
$ pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add the following environment variables:

``` bash 
SECRET_KEY=your_secret_key
ALGORITHM=HS256
MONGO_URI=your_mongodb_uri
DATABASE_NAME=candidate_management
```

5. Start the server:

``` bash 
$ uvicorn app.main:app --reload
```

6. Visit `http://localhost:8000/docs` to access the Swagger UI and test the API.

## API Endpoints

### User

- **POST /user/signup:**  Create a new user.
- **POST /user/login:** Login an existing user.

### Candidate

- **GET /candidate:** Get all candidates for the logged in user.
- **POST /candidate:** Create a new candidate for the logged in user.
- **PUT /candidate/{id}:** Update an existing candidate.
- **GET /candidate/{id}:** Get a single candidate by ID.
- **DELETE /candidate/{id}:** Delete a single candidate by ID.
- **GET /all-candidates:** Get all candidates.
- **GET /generate-report:** Generate a CSV report of all candidates.
## Authors

- Brandon Harrelson - [@Nodnarb1192](https://github.com/Nodnarb1192)

