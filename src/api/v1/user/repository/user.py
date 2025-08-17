from uuid import UUID
from sqlalchemy import select
from src.db.repository import AbstractRepository
from src.api.v1.user.model.user import User
from src.api.v1.user.model.user_progress import UserProgress


class UserRepository(AbstractRepository):
    model = User

    async def get_by_tg_id(self, tg_id: str):
        query = (
            select(
                self.model.id,
                self.model.username,
                UserProgress.last_book_id,
                UserProgress.last_page_id,
            )
            .outerjoin(UserProgress)
            .where(self.model.tg_id == tg_id)
        )
        result = await self._session.execute(query)
        return result.mappings().first()
