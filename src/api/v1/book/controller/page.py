from uuid import UUID
from fastapi import APIRouter, Depends
from src.api.v1.user.schema.user import UserRead
from src.api.v1.dependencies import get_current_user
from src.db.postgres import CurrentSession
from src.api.v1.book.schema.page import PageRead
from src.api.v1.book.service.page import PageService

router = APIRouter(
    prefix="/page",
    tags=["Страница"],
)


@router.get(
    "/{book_id}/last",
    response_model=PageRead,
)
async def get_last_page(
    book_id: UUID,
    session: CurrentSession,
):
    return await PageService(session).get_last_page(book_id)


@router.patch(
    "/{book_id}/next",
    response_model=PageRead,
)
async def get_next_page(
    book_id: UUID, session: CurrentSession, user: UserRead = Depends(get_current_user)
):
    return await PageService(session).get_next_page(book_id, user)


@router.patch(
    "/{book_id}/prev",
    response_model=PageRead,
)
async def get_prev_page(
    book_id: UUID,
    session: CurrentSession,
):
    return await PageService(session).get_prev_page(book_id)
