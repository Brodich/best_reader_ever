import uuid
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.v1.book.model.book import Book
from src.api.v1.user.model.user_progress import UserProgress
from src.db.base import MappedBase


class User(MappedBase):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    tg_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(nullable=True)

    books: Mapped[list[Book]] = relationship(
        "Book",
        back_populates="user",
        lazy="noload",
    )
    progress: Mapped[UserProgress] = relationship(  # type: ignore
        back_populates="user", uselist=False
    )
    questions: Mapped[list["Question"]] = relationship(back_populates="user")  # type: ignore
