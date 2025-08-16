# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import AsyncSession

# from db.base import Base

# DATABASE_URL = f"postgresql+asyncpg://hackaton:sample-pass@localhost/hackaton?async_fallback=True"
# engine = create_async_engine(DATABASE_URL)
# async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# async def get_session():
#     async with async_session() as session:
#         yield session


from typing import Annotated
from uuid import uuid4
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine

# from sqlalchemy.orm import sessionmaker

from common.model import MappedBase
from core.config import settings
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


def uuid4_str() -> str:
    return str(uuid4())
