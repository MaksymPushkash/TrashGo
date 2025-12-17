"""
Order Repository - Database access layer for Orders.

Extends BaseRepository with order-specific query methods.
Common CRUD operations are inherited from the base class.
"""

from typing import List
from sqlalchemy.orm import Session
from backend.app.models.order_model import Orders, OrderStatus
from backend.app.repository.base_repo import BaseRepository


class OrderRepository(BaseRepository[Orders]):
    """
    Inherits from BaseRepository:
        - get(db, id) -> get order by ID
        - get_all(db, skip, limit) -> list all orders
        - create(db, order) -> create new order
        - update(db, order) -> update existing order
        - delete(db, id) -> delete order by ID
    
    Custom methods:
        - get_by_user(db, user_id) -> orders for a specific user
        - get_by_courier(db, courier_id) -> orders for a specific courier
        - get_by_status(db, status) -> orders with a specific status
    """
    
    def __init__(self):
        super().__init__(Orders)


    def get_by_user(self, db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Orders]:
        return db.query(Orders).filter(Orders.user_id == user_id).offset(skip).limit(limit).all()


    def get_by_courier(self, db: Session, courier_id: str, skip: int = 0, limit: int = 100) -> List[Orders]:
        return db.query(Orders).filter(Orders.courier_id == courier_id).offset(skip).limit(limit).all()


    def get_by_status(self, db: Session, status: OrderStatus, skip: int = 0, limit: int = 100) -> List[Orders]:
        return db.query(Orders).filter(Orders.status == status).offset(skip).limit(limit).all()


order_repo = OrderRepository()
