import enum
import datetime
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.orm import relationship
from backend.app.db.session import Base


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    COURIER = "courier"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.datetime.now)
