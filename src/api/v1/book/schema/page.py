from typing import List
from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    total: int


class PageRead(BaseModel):
    id: str
    name: str
    content: List[str]
    pagination: Pagination
