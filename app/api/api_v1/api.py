from fastapi import APIRouter

from app.api.api_v1.endpoints import generation

api_router = APIRouter()
api_router.include_router(generation.router, prefix="/generation", tags=["generation"])