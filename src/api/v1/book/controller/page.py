from fastapi import APIRouter, Depends
from src.api.v1.book.schema.page import PageRead
from src.api.v1.book.service.page import page_service

router = APIRouter(
    prefix="/page",
    tags=["Страница"],
)


@router.get(
    "/{book_id}/last",
    response_model=PageRead,
)
async def get_page(
    # page: int,
):
    return await page_service.get_page()


# @router.get(
#     "/{book_id}",
#     response_model="",
# )
# async def get_page(
#     page: int,
# ):
#     return await page_service.get_page()
