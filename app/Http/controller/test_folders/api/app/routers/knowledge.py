from fastapi import APIRouter
from sqlalchemy.orm import Session
from . import models
from .schemas import KnowledgeCreate, Knowledge

router = APIRouter()

@router.post("/knowledge/")
async def create_knowledge(knowledge: KnowledgeCreate):
    db_knowledge = models.Knowledge(term=knowledge.term, description=knowledge.description)
    db.add(db_knowledge)
    await db.commit()
    return {"message": "Knowledge created successfully"}

@router.get("/knowledge/")
async def read_knowledge():
    knowledge = db.query(models.Knowledge).all()
    return [Knowledge.from_orm(knowledge) for knowledge in knowledge]