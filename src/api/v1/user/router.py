from fastapi import APIRouter

from src.api.v1.user.controller.user import router as user

v1 = APIRouter()

v1.include_router(user)
