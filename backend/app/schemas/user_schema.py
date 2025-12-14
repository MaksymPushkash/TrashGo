from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    role: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: str

    class Config:
        from_attributes = True






class UserVerification(BaseModel):
    password: str


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str
