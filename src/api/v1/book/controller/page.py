from typing import Optional
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/page",
    tags=["Страница"],
)


@router.get(
    "/all",
    response_model="",
)
async def get_page(
    page: int,
    user: Users = Depends(get_current_user),
):
    return await page_service.get_page(user, page)


