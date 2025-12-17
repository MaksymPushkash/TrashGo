"""
Auth Service - Authentication business logic.

This module handles authentication operations like
login, token creation, and token validation.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from backend.app.dependencies import DbSession
from backend.app.settings import jwt_config
from backend.app.models.user_model import Users
from backend.app.services import user_service


def authenticate_user(db: DbSession, username: str, password: str) -> Optional[Users]:
    return user_service.authenticate_user(db, username, password)


def create_access_token(username: str, user_id: str, role: str, expires_delta: timedelta) -> str:
    payload = {
        "sub": username,
        "id": user_id,
        "role": role,
        "exp": datetime.now() + expires_delta
    }

    return jwt.encode(payload, jwt_config.SECRET_KEY, algorithm=jwt_config.ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token, 
            jwt_config.SECRET_KEY, 
            algorithms=[jwt_config.ALGORITHM]
        )
        return payload

    except JWTError:
        return None


def get_token_data(token: str) -> Optional[dict]:
    payload = decode_token(token)
    
    if not payload:
        return None
    
    username = payload.get("sub")
    user_id = payload.get("id")
    user_role = payload.get("role")
    
    if not username or not user_id:
        return None
    
    return {"username": username, "user_id": user_id, "role": user_role}
