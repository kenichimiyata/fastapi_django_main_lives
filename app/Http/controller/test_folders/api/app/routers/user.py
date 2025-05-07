from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import models, schemas

router = APIRouter()

@router.post("/users/")
def create_user(user: schemas.UserSchema, db: Session = Depends()):
    db_user = models.User(username=user.username, password=user.password, profile=user.profile, team_id=user.team_id)
    db.add(db_user)
    db.commit()
    return {"message": "User created successfully"}

@router.get("/users/")
def read_users(db: Session = Depends()):
    users = db.query(models.User).all()
    return [{"username": user.username, "profile": user.profile} for user in users]

@router.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends()):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return {"message": "User not found"}
    return {"username": user.username, "profile": user.profile}**