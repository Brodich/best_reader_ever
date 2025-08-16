from fastapi import APIRouter, Depends
from src.db.postgres import CurrentSession
from src.api.v1.user.schema.user import UserRead, UserCreate
from src.api.v1.user.service.user import UserService

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)


@router.get(
    "",
    response_model=UserRead,
)
async def get_user(
    session: CurrentSession,
    user_id: str = "test",
):
    return await UserService(session).get_user(user_id)


@router.post(
    "",
    response_model=UserRead,
)
async def create_user(
    user: UserCreate,
    session: CurrentSession,
):
    return await UserService(session).create_user(user)
