import uuid
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from utils.logger import logger
from db.models.user import User
from db.db import get_session


app = FastAPI()


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


@app.post("/users", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = User(username=user.username)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@app.get("/users", response_model=List[UserRead])
async def list_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        # SQLAlchemy 2.0 ORM-style select
        User.__table__.select().offset(skip).limit(limit)
    )
    rows = result.fetchall()
    # rows = [Row(id=..., username=...)] → конвертируем в объекты User
    return [User(id=r.id, username=r.username) for r in rows]


@app.get("/hello")
def hello():
    logger.warning("Hello endpoint triggered")
    return "hello"
