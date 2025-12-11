from pydantic import BaseModel



class UserBase(BaseModel):
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str

class Config:
    orm_mode = True

