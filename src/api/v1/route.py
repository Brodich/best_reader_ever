from fastapi import APIRouter

from src.api.v1.user.router import v1 as user_v1
from src.api.v1.book.router import v1 as book_v1

from src.utils.settings import settings

route = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

route.include_router(user_v1)
route.include_router(book_v1)
