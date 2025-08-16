class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)  # правильный ответ
    difficulty: Mapped[int] = mapped_column(default=1)  # сложность вопроса (1-5)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="questions")
    book: Mapped["Book"] = relationship(back_populates="questions")
    page: Mapped["Page"] = relationship(back_populates="questions")
