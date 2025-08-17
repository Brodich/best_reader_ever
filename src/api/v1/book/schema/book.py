from uuid import UUID
from pydantic import BaseModel


class BookRead(BaseModel):
    id: UUID
    title: str
