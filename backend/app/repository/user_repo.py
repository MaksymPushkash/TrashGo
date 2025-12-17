"""
User Repository - Database access layer for Users.

Extends BaseRepository with user-specific query methods.
Common CRUD operations are inherited from the base class.
"""

from typing import Optional
from sqlalchemy.orm import Session
from backend.app.models.user_model import Users
from backend.app.repository.base_repo import BaseRepository


class UserRepository(BaseRepository[Users]):
    """
    Inherits from BaseRepository:
        - get(db, id) -> get user by ID
        - get_all(db, skip, limit) -> list all users
        - create(db, user) -> create new user
        - update(db, user) -> update existing user
        - delete(db, id) -> delete user by ID
    
    Custom methods:
        - get_by_email(db, email) -> find user by email
        - get_by_username(db, username) -> find user by username
    """
    
    def __init__(self):
        super().__init__(Users)


    def get_by_email(self, db: Session, email: str) -> Optional[Users]:
        return db.query(Users).filter(Users.email == email).first()


    def get_by_username(self, db: Session, username: str) -> Optional[Users]:
        return db.query(Users).filter(Users.username == username).first()


user_repo = UserRepository()
