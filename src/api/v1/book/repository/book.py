from uuid import UUID
from sqlalchemy import select
from src.db.repository import AbstractRepository
from src.api.v1.book.model.book import Book


class BookRepository(AbstractRepository):
    model = Book

    async def get_by_id(self, user_id: UUID):
        query = select(
            self.model.id,
            self.model.username,
        ).where(self.model.id == user_id)
        result = await self._session.execute(query)
        return result.mappings().first()
