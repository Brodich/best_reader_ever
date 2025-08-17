from typing import List
from uuid import UUID
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.book.schema.book import BookRead
from src.api.v1.book.utils.text_processor import TextProcessor
from src.api.v1.book.repository.book import BookRepository
from src.api.v1.book.repository.page import PageRepository


class BookService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_books(
        self,
    ):
        books: List[BookRead] = await BookRepository(self._session).get_all()
        return books

    async def create_book(
        self,
        file: UploadFile,
    ):
        if not file.filename.endswith(".txt"):
            return {"error": "Можно загружать только .txt файлы"}

        book: BookRead = await BookRepository(self._session).create(
            title=file.filename,
            author=None,
            user_id=UUID("ec0ade26-4042-4e48-a566-e1b77f3eaf6a"),
        )

        contents = await file.read()
        text = contents.decode("windows-1251")
        pages = TextProcessor().process(text)
        for i, page in enumerate(pages, start=1):
            await PageRepository(self._session).create(
                book_id=book.id,
                number=i,
                text=page,
            )

        # Тут можно сразу отправлять text в базу или дальше в обработку
        return book


book_service: BookService = BookService
