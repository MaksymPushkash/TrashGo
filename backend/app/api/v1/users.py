"""
Users API - REST endpoints for user operations.

All endpoints are async for consistency across the API.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from backend.app.dependencies import db_dependency, user_dependency
from backend.app.schemas.user_schema import UserRead
from backend.app.services import user_service


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserRead])
async def list_users(db: db_dependency) -> list[UserRead]:
    return user_service.list_users(db)


@router.get("/me", response_model=UserRead)
async def get_current_user_info(user: user_dependency, db: db_dependency) -> UserRead:
    user_data = user_service.get_user_by_id(db, user.get("user_id"))
    
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user_data


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: str, db: db_dependency) -> UserRead:
    user = user_service.get_user_by_id(db, user_id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, user: user_dependency, db: db_dependency):
    if user.get("user_id") != user_id and user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")
    
    deleted = user_service.delete_user(db, user_id)
    
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
