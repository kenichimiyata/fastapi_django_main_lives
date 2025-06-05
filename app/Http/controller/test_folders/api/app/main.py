from fastapi import FastAPI
from routers import user, team, knowledge

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}