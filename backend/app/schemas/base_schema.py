"""
Base Schema - Common Pydantic configuration for all schemas.
This module provides base classes that other schemas inherit from.
"""

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """
    Base schema for all Pydantic models.
    
    Provides common configuration. Extend this for schemas
    that don't need ORM conversion.
    """
    pass


class BaseReadSchema(BaseModel):
    """
    Base schema for "Read" responses that come from SQLAlchemy models.
    
    Includes from_attributes=True to allow automatic conversion
    from SQLAlchemy model instances to Pydantic schemas.
    
    Usage:
        class UserRead(BaseReadSchema):
            id: str
            email: str
    """
    
    class Config:
        from_attributes = True
