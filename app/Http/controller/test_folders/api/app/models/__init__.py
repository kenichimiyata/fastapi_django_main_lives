from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Base = declarative_base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)