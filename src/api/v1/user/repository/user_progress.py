from uuid import UUID
from sqlalchemy import select
from src.db.repository import AbstractRepository
from src.api.v1.user.model.user import User
from src.api.v1.user.model.user_progress import UserProgress


class UserProgressRepository(AbstractRepository):
    model = UserProgress

    # async def get_by_id(self, user_id: UUID):
    #     query = (
    #         select(
    #             self.model.id,
    #             self.model.username,
    #         )
    #         .outerjoin(UserProgress)
    #         .where(self.model.id == user_id)
    #     )
    #     result = await self._session.execute(query)
    #     return result.mappings().first()
