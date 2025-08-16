from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine

from src.db.base import MappedBase
from src.utils.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


DATABASE_URL = str(settings.database_url)

async_engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def create_table():
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)


async def get_session():
    async with async_session() as session:
        yield session


CurrentSession = Annotated[AsyncSession, Depends(get_session)]
