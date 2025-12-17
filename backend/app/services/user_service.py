"""
User Service - Business logic layer.

This module contains business logic for user operations.
It validates rules, transforms data, and calls the repository.

Uses custom exceptions for consistent error handling.
"""

from typing import Optional
from passlib.context import CryptContext
from backend.app.dependencies import DbSession
from backend.app.models.user_model import Users
from backend.app.repository.user_repo import user_repo
from backend.app.schemas.user_schema import UserRead, CreateUserRequest
from backend.app.utils.exceptions import NotFoundException, AlreadyExistsException, UnauthorizedException


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def create_user(db: DbSession, user_data: CreateUserRequest) -> Users:
    """
    1. Hash the password
    2. Create User model (UUID auto-generated)
    3. Save to database via repository
    """
    new_user = Users(
        email=user_data.email,
        username=user_data.username,
        role=user_data.role,
        hashed_password=hash_password(user_data.password)
    )

    return user_repo.create(db, new_user)


def get_user_by_id(db: DbSession, user_id: str) -> Optional[UserRead]:
    user = user_repo.get(db, user_id)

    if not user:
        return None
    return UserRead.model_validate(user)


def get_user_by_id_or_raise(db: DbSession, user_id: str) -> UserRead:
    user = user_repo.get(db, user_id)

    if not user:
        raise NotFoundException(f"User with id '{user_id}' not found")
    return UserRead.model_validate(user)


def get_user_by_email(db: DbSession, email: str) -> Optional[Users]:
    return user_repo.get_by_email(db, email)


def get_user_by_username(db: DbSession, username: str) -> Optional[Users]:
    return user_repo.get_by_username(db, username)


def list_users(db: DbSession, skip: int = 0, limit: int = 100) -> list[UserRead]:
    users = user_repo.get_all(db, skip=skip, limit=limit)
    return [UserRead.model_validate(u) for u in users]


def delete_user(db: DbSession, user_id: str) -> bool:
    return user_repo.delete(db, user_id)


def delete_user_or_raise(db: DbSession, user_id: str) -> None:
    deleted = user_repo.delete(db, user_id)
    if not deleted:
        raise NotFoundException(f"User with id '{user_id}' not found")


def authenticate_user(db: DbSession, username: str, password: str) -> Optional[Users]:
    user = user_repo.get_by_username(db, username)
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


def authenticate_user_or_raise(db: DbSession, username: str, password: str) -> Users:
    user = user_repo.get_by_username(db, username)
    
    if not user:
        raise UnauthorizedException("Invalid username or password")
    
    if not verify_password(password, user.hashed_password):
        raise UnauthorizedException("Invalid username or password")
    
    return user
