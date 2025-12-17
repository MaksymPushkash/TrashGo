"""
Dependencies - FastAPI dependency injection utilities.

This module centralizes all shared dependencies used across
API routes to avoid duplication (DRY principle).
"""

from typing import Annotated, Dict, Any
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.app.db.session import SessionLocal
from backend.app.security.auth import get_current_user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

DbSession = Session



# Authentication Dependencies

UserDict = Dict[str, Any]

user_dependency = Annotated[UserDict, Depends(get_current_user)]

