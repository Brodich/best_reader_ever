from datetime import datetime

# from uuid import UUID
from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from api.db.base import MappedBase


class User(MappedBase):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    tg_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(nullable=True)

    progress: Mapped["UserProgress"] = relationship(
        back_populates="user", uselist=False
    )
    questions: Mapped[list["Question"]] = relationship(back_populates="user")
