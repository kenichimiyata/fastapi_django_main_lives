from fastapi import FastAPI
from routers.user import router as user_router
from routers.team import router as team_router
from routers.knowledge import router as knowledge_router

app = FastAPI()

app.include_router(user_router)
app.include_router(team_router)
app.include_router(knowledge_router)