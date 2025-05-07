from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from database import SessionLocal
from models import User

router = APIRouter(prefix='/users')

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    username: str
    profile: str

@router.post('/register', response_class=RedirectResponse)
async def register_user(user: UserCreate, db: SessionLocal = Depends()):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail='Username already exists')
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url='/users', status_code=302)

@router.post('/login', response_class=RedirectResponse)
async def login_user(username: str, password: str, db: SessionLocal = Depends()):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail='Invalid username or password')
    return RedirectResponse(url='/users', status_code=302)

@router.get('/')
async def read_users(db: SessionLocal = Depends()):**
    users = db.query(User).all()
    return [UserRead(username=user.username, profile=user.profile) for user in users]

@router.get('/{username}')
async def read_user(username: str, db: SessionLocal = Depends()):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return UserRead(username=user.username, profile=user.profile)