"""
Order service layer.

Holds minimal business logic around orders and uses
repository helpers to interact with the database.
"""

import uuid
from typing import Iterable

from sqlalchemy.orm import Session

from backend.app.models.order_model import Orders
from backend.app.repository import order_repo
from backend.app.schemas.order_schema import OrderCreate, OrderRead


def create_order(db: Session, order_in: OrderCreate) -> OrderRead:
    """
    Create a new order and return it.

    Here we only generate an ID and call the repository.
    You can later add extra validation or side effects.
    """
    new_id = str(uuid.uuid4())
    db_order = order_repo.create_order(db, order_in, order_id=new_id)
    return OrderRead.model_validate(db_order)


def list_orders(db: Session) -> list[OrderRead]:
    """Return all orders as `OrderRead` objects."""
    orders: Iterable[Orders] = order_repo.list_orders(db)
    return [OrderRead.model_validate(o) for o in orders]


def get_order(db: Session, order_id: str) -> OrderRead | None:
    """Return a single order as `OrderRead` or None."""
    order = order_repo.get_order(db, order_id)
    if not order:
        return None
    return OrderRead.model_validate(order)

