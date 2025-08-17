from fastapi import HTTPException
from src.api.v1.user.repository.user import UserRepository
from src.api.v1.user.schema.user import UserCreate, UserRead
from src.db.postgres import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from src.api.v1.user.repository.user_progress import UserProgressRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user(
        self,
        tg_id: str,
    ):
        try:
            result: UserRead = await UserRepository(self._session).get_by_tg_id(tg_id)
            return result
        except NoResultFound:
            raise HTTPException(status_code=401, detail="User not found")

    async def create_user(
        self,
        user: UserCreate,
    ):
        try:
            result: UserRead = await UserRepository(self._session).create(
                **user.model_dump()
            )
            await UserProgressRepository(self._session).create(
                user_id=result.id,
                last_book_id=None,
            )
            return result
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists")
