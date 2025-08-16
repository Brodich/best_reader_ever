from fastapi import HTTPException
from src.api.v1.user.repository.user import UserRepository
from src.api.v1.user.schema.user import UserCreate, UserRead
from src.db.postgres import AsyncSession
from sqlalchemy.exc import IntegrityError


class UserService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user(
        self,
        user_id,
    ):
        result: UserRead = await UserRepository(self._session).get_by_id(user_id)
        return result

    async def create_user(
        self,
        user: UserCreate,
    ):
        # try:
        result: UserRead = await UserRepository(self._session).create(
            **user.model_dump()
        )
        print(result)
        return result
        # except IntegrityError:
        #     raise HTTPException(status_code=400, detail="User already exists")


# user_service: UserService = UserService
