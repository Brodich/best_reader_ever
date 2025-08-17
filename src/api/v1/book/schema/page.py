from typing import List
from uuid import UUID
from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    total: int


class PageRead(BaseModel):
    id: UUID
    number: int
    text: List[str]
    # pagination: Pagination
