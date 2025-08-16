from typing import Optional
from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres import get_session
from src.api.v1.user.model.user import User
from src.api.v1.user.schema.user import UserRead


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    user_id: Optional[str] = Header(None),
) -> UserRead | None:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не авторизован",
        )
    return user
