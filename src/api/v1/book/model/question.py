import uuid
from sqlalchemy import UUID
from datetime import datetime
from sqlalchemy import Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.postgres import MappedBase


class Question(MappedBase):
    __tablename__ = "questions"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"), nullable=False
    )
    page_id: Mapped[int] = mapped_column(
        ForeignKey("pages.id", ondelete="CASCADE"), nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(default=1)  # сложность вопроса (1-4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(  # type: ignore
        back_populates="questions",
        passive_deletes=True,
    )
    book: Mapped["Book"] = relationship(  # type: ignore
        back_populates="questions",
        passive_deletes=True,
    )
    page: Mapped["Page"] = relationship(  # type: ignore
        back_populates="questions",
        passive_deletes=True,
    )
