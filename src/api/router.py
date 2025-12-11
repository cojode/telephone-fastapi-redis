from fastapi.routing import APIRouter

from src.api.phone import router as phone_router

api_router = APIRouter(prefix="/api")

api_router.include_router(phone_router, prefix="/address", tags=["address"])
