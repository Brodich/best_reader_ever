from uuid import UUID
from fastapi import APIRouter, Depends
from src.db.postgres import CurrentSession
from src.api.v1.user.schema.user import UserRead, UserCreate
from src.api.v1.user.service.user_progress import UserProgressService

router = APIRouter(
    prefix="/progress",
    tags=["Прогресс"],
)


@router.patch(
    "/{book_id}/book",
    response_model=UserRead,
)
async def create_user(
    book_id: UUID,
    session: CurrentSession,
):
    return await UserProgressService(session).update_last_book(book_id)


@router.patch(
    "/{page_id}/page",
    response_model=UserRead,
)
async def create_user(
    page_id: UUID,
    session: CurrentSession,
):
    return await UserProgressService(session).update_last_page(page_id)
