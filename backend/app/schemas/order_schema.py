"""
Order Schemas - Pydantic models for order validation.

These schemas define the structure of order data
for API requests and responses.
"""

from typing import Optional
from pydantic import BaseModel

from backend.app.models.order_model import OrderStatus
from backend.app.schemas.base_schema import BaseReadSchema


class OrderCreate(BaseModel):
    courier_id: Optional[str] = None
    description: Optional[str] = None


class OrderRead(BaseReadSchema):
    id: str
    user_id: str
    courier_id: Optional[str] = None
    status: OrderStatus
    description: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderCourierAssign(BaseModel):
    courier_id: str
