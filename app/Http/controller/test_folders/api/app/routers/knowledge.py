from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import models, schemas

router = APIRouter()

@router.post("/knowledge/")
def create_knowledge(knowledge: schemas.KnowledgeSchema, db: Session = Depends()):
    db_knowledge = models.Knowledge(term=knowledge.term, description=knowledge.description)
    db.add(db_knowledge)
    db.commit()
    return {"message": "Knowledge created successfully"}

@router.get("/knowledge/")
def read_knowledge(db: Session = Depends()):
    knowledge = db.query(models.Knowledge).all()
    return [{"term": knowledge.term, "description": knowledge.description} for knowledge in knowledge]