from fastapi import APIRouter
from sqlalchemy.orm import Session
from . import models
from .schemas import TeamCreate, Team

router = APIRouter()

@router.post("/teams/")
async def create_team(team: TeamCreate):
    db_team = models.Team(name=team.name)
    db.add(db_team)
    await db.commit()
    return {"message": "Team created successfully"}

@router.get("/teams/")
async def read_teams():
    teams = db.query(models.Team).all()
    return [Team.from_orm(team) for team in teams]