from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker
from app.repositories.user import UserRepository
from app.services.user import UserService


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_repo(
        db: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(db=db)


async def get_user_service(
        user_repo: UserRepository = Depends(get_user_repo),
) -> UserService:
    return UserService(user_repo=user_repo)
