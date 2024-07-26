from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Login_Token_GetResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class Token_Data(BaseModel):
    user_email: str
    role_id: int
    working_status: bool

    class Config:
        from_attributes = True
