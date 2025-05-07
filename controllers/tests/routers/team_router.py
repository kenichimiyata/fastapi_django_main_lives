from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from database import SessionLocal
from models import Team

router = APIRouter(prefix='/teams')

class TeamCreate(BaseModel):
    name: str

class TeamRead(BaseModel):
    name: str
    created_at: str

@router.post('/', response_class=RedirectResponse)
async def create_team(team: TeamCreate, db: SessionLocal = Depends()):
    new_team = Team(name=team.name)
    db.add(new_team)
    db.commit()
    return RedirectResponse(url='/teams', status_code=302)

@router.get('/')
async def read_teams(db: SessionLocal = Depends()):
    teams = db.query(Team).all()
    return [TeamRead(name=team.name, created_at=team.created_at) for team in teams]