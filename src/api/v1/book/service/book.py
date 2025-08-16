from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


class BookService:
    @staticmethod
    async def get_books():
        pass

    @staticmethod
    async def get_book():
        pass

    @staticmethod
    async def create_book(
        session: AsyncSession,
        file: UploadFile,
    ):
        if not file.filename.endswith(".txt"):
            return {"error": "Можно загружать только .txt файлы"}
        contents = await file.read()
        text = contents.decode("utf-8")  # предполагаем UTF-8

        # Тут можно сразу отправлять text в базу или дальше в обработку
        return {"filename": file.filename, "content": text}


book_service: BookService = BookService
