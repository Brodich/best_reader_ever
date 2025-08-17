from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UserRead(BaseModel):
    id: UUID
    username: Optional[str] | None
    last_book_id: Optional[UUID] | None
    last_page_id: Optional[UUID] | None


class UserCreate(BaseModel):
    tg_id: str
    username: Optional[str] | None
