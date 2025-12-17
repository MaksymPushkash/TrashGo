"""
Order Model - SQLAlchemy model for orders.

Defines the database schema for the orders table.
"""

import enum
import uuid
from sqlalchemy import Column, Enum, ForeignKey, String
from backend.app.db.session import Base


class OrderStatus(str, enum.Enum):
    CREATED = "created"
    ASSIGNED = "assigned"
    PICKED_UP = "picked_up"
    COMPLETED = "completed"
    CANCELED = "canceled"


class Orders(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    courier_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED, nullable=False)
    description = Column(String, nullable=True)

