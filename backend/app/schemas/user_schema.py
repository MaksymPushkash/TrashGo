"""
User Schemas - Pydantic models for user validation.

These schemas define the structure of user data
for API requests and responses.

Note: Token schema moved to auth_schema.py (Interface Segregation)
"""

from typing import Optional
from pydantic import BaseModel, field_validator

from backend.app.models.user_model import UserRole
from backend.app.schemas.base_schema import BaseReadSchema


class UserBase(BaseModel):
    """Base schema with common user fields."""
    email: str
    username: str


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        """Ensure role is a valid UserRole enum value."""
        valid_roles = [r.value for r in UserRole]
        if value not in valid_roles:
            raise ValueError(f"Invalid role. Must be one of: {valid_roles}")
        return value


class UserRead(BaseReadSchema):
    id: str
    email: str
    username: Optional[str] = None
    role: UserRole


class UserUpdate(BaseModel):
    email: str | None = None
    username: str | None = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str
