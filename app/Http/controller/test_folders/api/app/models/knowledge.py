from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Knowledge(Base):
    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True)
    term = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Knowledge(term={self.term}, description={self.description})"