from fastapi import APIRouter

from src.api.v1.user.controller.user import router as user
# from app.orders.api.v1.template import router as template

v1 = APIRouter()

v1.include_router(user)
# v1.include_router(template)
