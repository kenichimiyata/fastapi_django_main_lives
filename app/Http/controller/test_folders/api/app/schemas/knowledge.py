from pydantic import BaseModel

class KnowledgeSchema(BaseModel):
    term: str
    description: str
    created_at: datetime

    class Config:
        orm_mode = True