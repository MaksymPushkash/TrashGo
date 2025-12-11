from sqlalchemy import Column, String, Enum, ForeignKey
from backend.app.db.session import Base
import enum

class OrderStatus(str, enum.Enum):
    CREATED = "created"
    ASSIGNED = "assigned"
    PICKED_UP = "picked_up"
    COMPLETED = "completed"
    CANCELED = "canceled"

class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    courier_id = Column(String, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED)
    description = Column(String, nullable=True)


