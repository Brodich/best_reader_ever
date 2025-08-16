from abc import ABC, abstractmethod
from typing import Any, List

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# from sqlalchemy.sql import type_coerce


class AbstractRepository(ABC):
    def __init__(self, session: Session):
        self._session = session

    model = None

    async def commit(self):
        try:
            await self._session.commit()
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise e

    def rollback(self):
        self._session.rollback()

    async def get_by_id(self, id):
        return await self._session.get(self.model, id)

    async def get_all(self) -> List[Any]:
        result = await self._session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, **obj):
        query = insert(self.model).values(**obj).returning(self.model)
        result = await self._session.execute(query)
        await self._session.commit()
        return result.scalars().first()

    async def update_one(self, id, **obj):
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj)
            .returning(self.model)
        )
        result = await self._session.execute(query)
        return result.scalars().first()

    async def delete_by_id(self, id):
        result = await self._session.execute(
            delete(self.model).where(self.model.id == id)
        )
        return result.rowcount

    async def get_by_filter(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self._session.execute(query)
        return result.scalars().all()
