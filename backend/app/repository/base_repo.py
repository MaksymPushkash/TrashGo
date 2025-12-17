"""
Base Repository - Abstract base for repositories.

This module provides common CRUD operations that can be
inherited by specific repositories.

All child repositories should extend this class and:
- Call super().__init__(Model) with their model class
- Add only model-specific query methods
"""

from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from backend.app.db.session import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()


    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()


    def create(self, db: Session, obj: ModelType) -> ModelType:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj


    def update(self, db: Session, obj: ModelType) -> ModelType:
        db.commit()
        db.refresh(obj)
        return obj


    def delete(self, db: Session, id: str) -> bool:
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

