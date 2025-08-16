from typing import Optional
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/book",
    tags=["Книга"],
)


@router.get(
    "/all",
    response_model="",
)
async def get_books(
    user: Users = Depends(get_current_user),
):
    return await book_service.get_books(user)


@router.get(
    "/upload",
    response_model="",
)
async def create_book(
    user: Users = Depends(get_current_user),
):
    return await book_service.create_book()


@router.get(
    "/{book_id}",
    response_model="",
)
async def get_book(
    user: Users = Depends(get_current_user),
):
    return await claim_service.get_book(user)
