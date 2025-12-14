"""
Users service layer.

This module contains simple business logic functions
that:
- validate high-level rules
- call repository helpers
- prepare data for the API layer
"""

import uuid
from typing import Iterable

from sqlalchemy.orm import Session

from backend.app.models.user_model import Users
from backend.app.repository import user_repo
from backend.app.schemas.user_schema import UserCreate, UserRead


def _fake_hash_password(raw_password: str) -> str:
    """
    Very simple password "hashing".

    IMPORTANT:
    - This is only a placeholder for the base structure.
    - Replace with real hashing (e.g. bcrypt) later.
    """

    return f"hashed-{raw_password}"


def create_user(db: Session, user_in: UserCreate) -> UserRead:
    """
    Create a new user.

    Steps:
    - generate UUID
    - hash password
    - call repository
    - convert ORM model to `UserRead`
    """

    new_id = str(uuid.uuid4())
    user_in_for_repo = UserCreate(
        email=user_in.email,
        role=user_in.role,
        password=_fake_hash_password(user_in.password),
    )
    db_user = user_repo.create_user(db, user_in_for_repo, user_id=new_id)
    return UserRead.model_validate(db_user)


def list_users(db: Session) -> list[UserRead]:
    """Return all users as `UserRead` objects."""
    users: Iterable[Users] = user_repo.list_users(db)
    return [UserRead.model_validate(u) for u in users]


def get_user(db: Session, user_id: str) -> UserRead | None:
    """Return a single user as `UserRead` or None."""
    user = user_repo.get_user(db, user_id)
    if not user:
        return None
    return UserRead.model_validate(user)

