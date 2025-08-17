import uuid
from sqlalchemy import ARRAY, UUID
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.postgres import MappedBase


class Page(MappedBase):
    __tablename__ = "pages"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"), nullable=False
    )
    number: Mapped[int] = mapped_column(nullable=False)
    text: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)

    book: Mapped["Book"] = relationship(back_populates="pages")  # type: ignore
    questions: Mapped[list["Question"]] = relationship(back_populates="page")  # type: ignore
