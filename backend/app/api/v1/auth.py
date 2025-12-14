from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.dependencies import db_dependency
from backend.app.models.user_model import Users
from backend.app.schemas.user_schema import CreateUserRequest
from backend.app.security.auth import bcrypt_context, authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])




@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(email=create_user_request.email,
                              username=create_user_request.username,
                              role=create_user_request.role,
                              hashed_password=bcrypt_context.hash(create_user_request.password),
                              is_active=True)

    db.add(create_user_model)
    db.commit()





@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}