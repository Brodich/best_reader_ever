from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from src.api.v1.book.schema.book import BookRead
from src.api.v1.dependencies import get_current_user
from src.api.v1.user.schema.user import UserRead
from src.db.postgres import CurrentSession
from src.api.v1.book.service.book import BookService

router = APIRouter(
    prefix="/book",
    tags=["Книга"],
)


@router.get(
    "/all",
    response_model=List[BookRead],
)
async def get_books(
    session: CurrentSession,
    # user: UserRead = Depends(get_current_user),
):
    return await BookService(session).get_books()


@router.post(
    "/upload",
    response_model=BookRead,
)
async def create_book(
    session: CurrentSession,
    file: UploadFile = File(...),
    # user: UserRead = Depends(get_current_user),
):
    return await BookService(session).create_book(
        file,
    )
