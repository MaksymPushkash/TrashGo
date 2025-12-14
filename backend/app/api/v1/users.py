from typing import List
from fastapi import APIRouter, HTTPException, status
from backend.app.dependencies import db_dependency
from backend.app.schemas.user_schema import UserCreate, UserRead
from backend.app.services import user_service


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: db_dependency) -> UserRead:
    return user_service.create_user(db, user_in)


@router.get("/", response_model=List[UserRead])
def list_users(db: db_dependency) -> list[UserRead]:
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, db: db_dependency) -> UserRead:
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
    return user
