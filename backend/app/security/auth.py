"""
Security Auth - Authentication utilities for FastAPI.

This module provides FastAPI dependencies for authentication:
- OAuth2 password bearer scheme
- get_current_user dependency for protected routes
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.app.services import auth_service


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> dict:
    token_data = auth_service.get_token_data(token)
    
    if not token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    return token_data
