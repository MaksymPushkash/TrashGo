"""
Auth API - REST endpoints for authentication.

Handles user registration and login.
All endpoints are async for consistency across the API.
"""

from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.dependencies import db_dependency
from backend.app.schemas.user_schema import CreateUserRequest
from backend.app.schemas.auth_schema import Token
from backend.app.services import user_service, auth_service


router = APIRouter(prefix="/auth", tags=["auth"])


ACCESS_TOKEN_EXPIRE_MINUTES = 20



@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(db: db_dependency, create_user_request: CreateUserRequest):
    existing_user = user_service.get_user_by_email(db, create_user_request.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    existing_username = user_service.get_user_by_username(db, create_user_request.username)
    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    user_service.create_user(db, create_user_request)
    
    return {"message": "User created successfully"}



@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    token = auth_service.create_access_token(
        username=user.username,
        user_id=user.id,
        role=user.role.value,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": token, "token_type": "bearer"}
