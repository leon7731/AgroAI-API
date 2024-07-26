from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

# My Functions
from Schemas import auth_schema

# Config Folder
from Config.Config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # Create an OAuth2 scheme

# Secret key for signing JWT tokens
Secret_Key = settings.secret_key # Secret key to sign JWT tokens
ALGORITHM = settings.ALGORITHM  # Algorithm to use for signing JWT tokens
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes # Expiration time for JWT tokens # 1440 minutes = 24 hours



def Create_Access_Token(data: dict):
    """_summary_: Create a JWT token
    Args:
        data (dict): Required data to create the token
    Returns:
        _type_: str
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # Calculate the expiration time
    to_encode.update({"exp": expire}) 
    encoded_jwt = jwt.encode(to_encode, Secret_Key, algorithm=ALGORITHM) 
    return encoded_jwt


def Verify_Access_Token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, Secret_Key, algorithms=[ALGORITHM])
        user_email: str = payload.get("user_email")
        role_id: int = payload.get("role_id")
        working_status: bool = payload.get("working_status")
        
        if None in [user_email, role_id, working_status]:
            raise credentials_exception
        
        token_data = auth_schema.Token_Data(user_email=user_email, 
                                            role_id=role_id, 
                                            working_status=working_status)
        return token_data
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    

def Get_Current_User(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = Verify_Access_Token(token, credentials_exception = credentials_exception) 
    
    # print(f"token: {token.user_email}")
    return token
    
    
    
     
