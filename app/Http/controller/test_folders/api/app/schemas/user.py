from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    password: str
    profile: str
    tags: str
    team_id: int

**api/app/schemas/team.py**