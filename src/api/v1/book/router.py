from fastapi import APIRouter

from src.api.v1.book.controller.book import router as book
from src.api.v1.book.controller.page import router as page
from src.api.v1.book.controller.question import router as question

v1 = APIRouter()

v1.include_router(book)
v1.include_router(page)
v1.include_router(question)
