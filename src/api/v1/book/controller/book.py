from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from src.api.v1.book.schema.book import BookRead
from src.api.v1.dependencies import get_current_user
from src.api.v1.user.schema.user import UserRead
from src.db.postgres import get_session
from src.api.v1.book.service.book import book_service
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/book",
    tags=["Книга"],
)


@router.get(
    "/all",
    response_model=List[BookRead],
)
async def get_books(
    user: UserRead = Depends(get_current_user),
):
    return await book_service.get_books()


@router.post(
    "/upload",
    response_model=BookRead,
)
async def create_book(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    user: UserRead = Depends(get_current_user),
):
    return await book_service.create_book(
        session,
        file,
    )


# @router.get(
#     "/{book_id}",
#     response_model="",
# )
# async def get_book():
#     return await book_service.get_book()
