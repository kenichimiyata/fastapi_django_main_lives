from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    profile = Column(String)
    tags = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", backref="users")