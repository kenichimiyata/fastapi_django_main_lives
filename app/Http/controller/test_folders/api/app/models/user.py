from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    profile = Column(String)
    tags = Column(String)

    def __init__(self, password, profile, tags):
        self.username = username
        self.password = password
        self.profile = profile
        self.tags = tags