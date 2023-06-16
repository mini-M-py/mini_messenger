from pydantic import BaseModel, EmailStr

class create_user(BaseModel):
    user_name: str
    email: EmailStr
    password: str

class user_out(BaseModel):
    user_name: str

    class Config:
        orm_mode = True