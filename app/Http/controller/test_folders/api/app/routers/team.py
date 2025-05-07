from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import models, schemas

router = APIRouter()

@router.post("/teams/")
def create_team(team: schemas.TeamSchema, db: Session = Depends()):
    db_team = models.Team(name=team.name)
    db.add(db_team)
    db.commit()
    return {"message": "Team created successfully"}

@router.get("/teams/")
def read_teams(db: Session = Depends()):
    teams = db.query(models.Team).all()
    return [{"name": team.name, "created_at": team.created_at} for team in teams]