from uuid import UUID
from sqlalchemy import select
from src.db.repository import AbstractRepository
from src.api.v1.book.model.page import Page


class PageRepository(AbstractRepository):
    model = Page

    async def get_last_page(self, book_id: UUID):
        query = (
            select(self.model.id, self.model.text, self.model.number)
            .where(self.model.book_id == book_id)
            .limit(1)
        )
        result = await self._session.execute(query)
        return result.mappings().first()

    async def get_next_page(self, book_id: UUID, current_page: int):
        query = (
            select(self.model.id, self.model.text, self.model.number)
            .where(self.model.book_id == book_id)
            .where(self.model.number == current_page + 1)
            .limit(1)
        )
        result = await self._session.execute(query)
        return result.mappings().first()

    async def get_prev_page(self, book_id: UUID, current_number: int):
        query = (
            select(self.model.id, self.model.text, self.model.number)
            .where(self.model.book_id == book_id)
            .where(self.model.number == current_number - 1)
            .limit(1)
        )
        result = await self._session.execute(query)
        return result.mappings().first()
