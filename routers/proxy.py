from fastapi import APIRouter, Request, HTTPException
import httpx

LARAVEL_URL = "http://localhost:8000"

router = APIRouter(prefix="/gradios", tags=["gradios"])

@router.api_route("/route/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        req_data = await request.body()
        try:
            proxied = await client.request(
                request.method,
                f"{LARAVEL_URL}/{path}",
                headers=request.headers.raw,
                content=req_data
            )
            # ステータスコードやヘッダも引き継ぎたい場合は調整してください
            return proxied.text
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request proxy failed: {str(e)}")
