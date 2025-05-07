from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    profile = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", backref="users")

    def __repr__(self):
        return f"User(username={self.username}, profile={self.profile})"