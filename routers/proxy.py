import httpx
#from fastapi import FastAPI, Request


import requests
import json
import os
# current_user: User = Depends(get_current_active_user)):
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# current_user: User = Depends(get_current_active_user)):
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

from fastapi import APIRouter, HTTPException
from gradio_client import Client

#router = APIRouter()
router = APIRouter(prefix="/gradio", tags=["gradio"])
@router.get("/route/proxy")

#LARAVEL_URL="http://localhost:8000"
LARAVEL_URL="http://localhost:8000"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path: str):
    client = httpx.AsyncClient()
    req_data = await request.body()
    proxied = await client.request(
        request.method,
        f"{LARAVEL_URL}/{path}",
        headers=request.headers.raw,
        content=req_data
    )
    return proxied.text
