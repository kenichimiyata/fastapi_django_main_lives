from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    __init__(self, name):
        self.name = name