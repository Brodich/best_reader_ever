from uuid import UUID
from src.api.v1.user.service.user_progress import UserProgressService
from src.api.v1.book.repository.page import PageRepository
from sqlalchemy.ext.asyncio import AsyncSession


class PageService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_last_page(self, book_id: UUID):
        page = await PageRepository(self._session).get_last_page(book_id)
        return page

    async def get_next_page(self, book_id: UUID, user):
        current_page = UserProgressService(self._session).get_progress(user.id)
        page = await PageRepository(self._session).get_next_page(book_id, current_page)
        return page

    async def get_prev_page(self, book_id: UUID, current_number: int):
        page = await PageRepository(self._session).get_prev_page(
            book_id, current_number
        )
        return page


page_service: PageService = PageService
