import datetime
import enum
from sqlalchemy import Column, DateTime, Enum, String
from backend.app.db.session import Base


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    COURIER = "courier"


class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)




