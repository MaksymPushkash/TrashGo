from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users():
    return {"message": "List users here"}