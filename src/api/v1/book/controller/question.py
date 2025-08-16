from typing import Optional
from fastapi import APIRouter, Depends
from src.api.v1.book.service.question import question_service

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
    # user: Users = Depends(get_current_user),
):
    return await question_service.get_questions(page)


@router.get(
    "/{question_id}",
    response_model="",
)
async def get_question(
    page: int,
    # user: Users = Depends(get_current_user),
):
    return await question_service.get_question(page)


@router.get(
    "/{question_id}/answer",
    response_model="",
)
async def get_answer(
    page: int,
    # user: Users = Depends(get_current_user),
):
    return await question_service.get_answer(page)
