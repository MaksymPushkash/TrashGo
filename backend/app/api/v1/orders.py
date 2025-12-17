"""
Orders API - REST endpoints for order operations.

All endpoints are async for consistency across the API.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from backend.app.dependencies import db_dependency, user_dependency
from backend.app.schemas.order_schema import OrderRead, OrderCreate, OrderStatusUpdate
from backend.app.services import order_service


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, user: user_dependency, db: db_dependency):
    order = order_service.create_order(db, order_data, user.get("user_id"))
    return OrderRead.model_validate(order)


@router.get("/", response_model=List[OrderRead])
async def list_orders(db: db_dependency) -> list[OrderRead]:
    return order_service.list_orders(db)


@router.get("/my", response_model=List[OrderRead])
async def list_my_orders(user: user_dependency, db: db_dependency) -> list[OrderRead]:
    return order_service.list_user_orders(db, user.get("user_id"))


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: str, db: db_dependency) -> OrderRead:
    order = order_service.get_order_by_id(db, order_id)
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    return order


@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_order_status(order_id: str, status_update: OrderStatusUpdate, user: user_dependency, db: db_dependency) -> OrderRead:
    if user.get("role") not in ["courier", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only couriers and admins can update order status")
    
    order = order_service.update_order_status(db, order_id, status_update.status)
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    return order


@router.patch("/{order_id}/assign", response_model=OrderRead)
async def assign_courier(order_id: str, user: user_dependency, db: db_dependency) -> OrderRead:
    if user.get("role") != "courier":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only couriers can assign themselves to orders")
    
    order = order_service.assign_courier(db, order_id, user.get("user_id"))
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: str, user: user_dependency, db: db_dependency):
    order = order_service.get_order_by_id(db, order_id)
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.user_id != user.get("user_id") and user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this order")
    
    order_service.delete_order(db, order_id)
