from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    profile: str
    tags: str

class User(UserCreate):
    id: int
    username: str
    profile: str
    tags: str