# FastAPI
from fastapi import Depends, status, Response, HTTPException, APIRouter

# # OAuth2
# from Functions.oauth2 import oauth2_scheme
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# Database
from sqlalchemy.orm import Session
from Database.Database_Engine import get_db

from Database import users_database

# Schema
from Schemas import auth_schema


# My Functions
from Functions import General_Func as GF
from Functions import oauth2


### Auth Router ###
router = APIRouter(tags = ["Authentication"]) 

        
### Auth - Login ###
@router.post("/auth/login", status_code=status.HTTP_200_OK, 
            # response_model=auth_schema.Custom_Auth_GET_Response
            )
def login(response: Response, user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  try:

    # Hash the password
    hashed_password = GF.HashPassword_SHA256(user_credentials.password)

    # Find the User with the Email & Password
    user_query = db.query(users_database.Users_Table).filter(
      users_database.Users_Table.email == user_credentials.username,
      users_database.Users_Table.password == hashed_password).first()
    
    if not user_query: # If the User is not available
      response.status_code = status.HTTP_403_FORBIDDEN
      return {'status': 'error',
              'message': 'Invalid Credentials'
            }
      
    else:  # If the User is available
      access_token = oauth2.Create_Access_Token(data={"user_email": user_query.email, 
                                                      "role_id": user_query.role,
                                                      "working_status": user_query.working_status})
      
      # print(f"user_query: {user_query.working_status}")
      response.status_code = status.HTTP_200_OK
      return {'status': 'success',
              'access_token': access_token,
              'token_type': 'bearer'
            }
    
  except Exception as e:
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {'status': 'error',
            'message': 'Data Not Fetched',
            'data': []}








