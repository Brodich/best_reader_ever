from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class UserRead(BaseModel):
    id: UUID
    # tg_id: str
    username: Optional[str] | None


class UserCreate(BaseModel):
    tg_id: str
    username: Optional[str] | None
