from datetime import datetime
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str | None] = mapped_column(nullable=True)

    pages: Mapped[list["Page"]] = relationship(back_populates="book")
    questions: Mapped[list["Question"]] = relationship(back_populates="book")
