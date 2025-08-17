from fastapi import APIRouter

from src.api.v1.user.controller.user import router as user
from src.api.v1.user.controller.user_progress import router as progress

v1 = APIRouter()

v1.include_router(user)
v1.include_router(progress)
