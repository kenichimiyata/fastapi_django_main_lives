from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Knowledge(Base):
    __tablename__ = "knowledge"
    id = Column(Integer, primary_key=True)
    term = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)