from fastapi import APIRouter, Depends
from src.api.v1.user.schema.user import UserRead
from src.api.v1.user.service.user import user_service

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)


@router.get(
    "",
    response_model=UserRead,
)
async def get_user():
    return await user_service.get_user()
