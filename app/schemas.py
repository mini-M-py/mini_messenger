from typing import Optional
from pydantic import BaseModel, EmailStr

class create_user(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    otp:str

class user_out(BaseModel):
    id: int
    user_name: str

    class Config:
        orm_mode = True

class verify(BaseModel):
    email:EmailStr

class forget_password(BaseModel):
    email: EmailStr
    new_password: str
    otp: str

class delete_user(BaseModel):

    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Token_data(BaseModel):
    id: Optional[str] = None