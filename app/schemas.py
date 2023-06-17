from pydantic import BaseModel, EmailStr

class create_user(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    otp:str

class user_out(BaseModel):
    user_name: str

    class Config:
        orm_mode = True

class verify(BaseModel):
    email:EmailStr