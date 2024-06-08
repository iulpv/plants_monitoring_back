from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def hello():
    return {"message": "Service for determining plant health."}
