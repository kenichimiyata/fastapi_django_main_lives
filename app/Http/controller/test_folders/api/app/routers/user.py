from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from . import models
from .schemas import UserCreate, User

router = APIRouter()

@router.post("/users/")
async def create_user(user: UserCreate):
    db_user = models.User(username=user.username, password=user.password, profile=user.profile, tags=user.tags)
    db.add(db_user)
    await db.commit()
    return {"message": "User created successfully"}

@router.get("/users/")
async def read_users():
    users = db.query(models.User").all()
    return [User.from_orm(user) in users]

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User.from_orm(user)