from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = (
            select(User)
            .where(User.id == user_id)
        )

        user = (await self.db.execute(query)).scalar_one_or_none()
        return user

    async def get_active_user_by_id(self, user_id: int) -> User | None:
        query = (
            select(User)
            .where(User.id == user_id)
            .where(User.is_active == True)
        )

        user = (await self.db.execute(query)).scalar_one_or_none()
        return user
