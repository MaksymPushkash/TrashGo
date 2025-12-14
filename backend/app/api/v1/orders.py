from typing import Annotated, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.dependencies import get_db
from backend.app.schemas.order_schema import OrderRead, OrderBase
from backend.app.services import order_service
from backend.app.models.order_model import Orders
from backend.app.security.auth import get_current_user
from backend.app.dependencies import db_dependency


router = APIRouter(prefix="/orders", tags=["orders"])




UserDict = Dict[str, Any]
user_dependency = Annotated[UserDict, Depends(get_current_user)]




# ТУТ ПОМИЛКА

@router.post("/order", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(order_base: OrderBase, user: user_dependency, db: db_dependency):
    
    order_model = Orders(**order_base.model_dump(), user_id=user.get('user_id'))
    db.add(order_model)
    db.commit()
    db.refresh(order_model)

    return order_model




@router.get("/", response_model=List[OrderRead])
async def list_orders(db: db_dependency) -> list[OrderRead]:
    return order_service.list_orders(db)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: str, db: db_dependency) -> OrderRead:
    order = order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

