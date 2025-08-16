from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.v1.book.model.page import Page
from src.api.v1.book.model.question import Question

from src.db.postgres import MappedBase


class Book(MappedBase):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str | None] = mapped_column(nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="books")
    pages: Mapped[list[Page]] = relationship(back_populates="book")
    questions: Mapped[list[Question]] = relationship(back_populates="book")
