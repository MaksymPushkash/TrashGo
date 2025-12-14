from typing import Iterable, Optional
from sqlalchemy.orm import Session
from backend.app.models.order_model import Orders
from backend.app.schemas.order_schema import OrderCreate


def create_order(db: Session, order_in: OrderCreate, *, order_id: str) -> Orders:
    """
    Create and persist a new order.

    `order_id` is generated in the service layer.
    """
    db_order = Orders(
        id=order_id,
        user_id=order_in.user_id,
        courier_id=order_in.courier_id,
        status=order_in.status,
        description=order_in.description,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: str) -> Optional[Orders]:
    """Return order by id or None."""
    return db.get(Orders, order_id)


def list_orders(db: Session, *, skip: int = 0, limit: int = 100) -> Iterable[Orders]:
    """Return a slice of orders."""
    return db.query(Orders).offset(skip).limit(limit).all()


def delete_order(db: Session, order_id: str) -> bool:
    """
    Delete order by id.

    Returns True if deleted, False otherwise.
    """
    order = get_order(db, order_id)
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True

