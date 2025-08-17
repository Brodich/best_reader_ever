from uuid import UUID
from fastapi import HTTPException
from src.api.v1.user.repository.user_progress import UserProgressRepository
from src.api.v1.user.schema.user import UserCreate, UserRead
from src.db.postgres import AsyncSession
from sqlalchemy.exc import IntegrityError


class UserProgressService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_progress(
        self,
        user_id,
    ):
        result: UserRead = await UserProgressRepository(self._session).get_by_id(
            user_id
        )
        return result

    async def update_last_book(self, book_id: UUID):
        progress_id = await self.get_progress()
        result = await UserProgressRepository(self._session).update_one(
            id=progress_id,
            last_book_id=book_id,
        )
        return result

    async def update_last_page(self, page_id: UUID):
        progress_id = await self.get_progress()
        result = await UserProgressRepository(self._session).update_one(
            id=progress_id,
            last_page_id=page_id,
        )
        return result


# user_service: UserService = UserService
