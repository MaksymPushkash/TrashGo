"""
Auth Schemas - Pydantic models for authentication.

These schemas define the structure of authentication data
for API requests and responses.
"""

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for decoded token payload."""
    username: str | None = None
    user_id: str | None = None
    role: str | None = None
