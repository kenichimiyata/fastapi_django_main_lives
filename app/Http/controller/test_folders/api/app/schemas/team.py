from pydantic import BaseModel

class TeamCreate(BaseModel):
    name: str

class Team(TeamCreate):
    id: int
    name: str