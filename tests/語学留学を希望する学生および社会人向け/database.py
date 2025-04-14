from app import db

def create_database():
    db.create_all()

def query_database(query):
    return db.session.execute(query)