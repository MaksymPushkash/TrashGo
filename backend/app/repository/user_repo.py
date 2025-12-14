"""
Users repository.

This layer isolates raw SQLAlchemy operations.
Service functions should call these helpers instead of
working with the session directly.
"""

from typing import Iterable, Optional
from sqlalchemy.orm import Session
from backend.app.models.user_model import Users
from backend.app.schemas.user_schema import UserCreate


def create_user(db: Session, user_in: UserCreate, *, user_id: str) -> Users:
    """
    Create and persist a new user.

    NOTE:
    - `user_id` is generated outside (service layer).
    - `user_in.password` must already be hashed before calling this.
    """

    db_user = Users(
        id=user_id,
        email=user_in.email,
        hashed_password=user_in.password,  # replace with real hash in service
        role=user_in.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: str) -> Optional[Users]:
    """Return user by id or None."""
    return db.get(Users, user_id)


def get_user_by_email(db: Session, email: str) -> Optional[Users]:
    """Return user by email or None."""
    return db.query(Users).filter(Users.email == email).first()


def list_users(db: Session, *, skip: int = 0, limit: int = 100) -> Iterable[Users]:
    """Return a slice of users for simple pagination."""
    return db.query(Users).offset(skip).limit(limit).all()


def delete_user(db: Session, user_id: str) -> bool:
    """
    Delete user by id.

    Returns:
        True if a row was deleted, False otherwise.
    """
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True

