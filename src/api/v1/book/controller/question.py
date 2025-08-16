from typing import Optional
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/question",
    tags=["Вопросы по пройденному материалу"],
)


@router.get(
    "/all",
    response_model="",
)
async def get_questions(
    page: int,
    user: Users = Depends(get_current_user),
):
    return await page_service.get_questions(user, page)

@router.get(
    "/all",
    response_model="",
)
async def get_question(
    page: int,
    user: Users = Depends(get_current_user),
):
    return await page_service.get_question(user, page)
