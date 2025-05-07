from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from database import SessionLocal, engine
from models import User, Team
from routers import user_router, team_router = APIRouter(prefix='/teams')

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    database.Base.metadata.create_all(bind=engine)

@app.get('/')
async def root():
    return {'message': 'Welcome to the API'}