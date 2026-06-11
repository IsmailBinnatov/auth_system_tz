from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User, Role, UserRole, TokenBlacklist


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

    async def get_active_user_by_email(self, email: str) -> User | None:
        query = (
            select(User)
            .where(User.email == email)
            .where(User.is_active == True)
        )
        user = (await self.db.execute(query)).scalar_one_or_none()
        return user

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        return user

    async def assign_role_to_user(self, user_id: int, role_name: str) -> None:
        query = (
            select(Role)
            .where(Role.name == role_name)
        )
        role = (await self.db.execute(query)).scalar_one_or_none()
        if not role:
            raise ValueError(f'Role \'{role_name}\' not found')

        user_role = UserRole(
            user_id=user_id,
            role_id=role.id,
        )

        self.db.add(user_role)

    async def flush(self):
        await self.db.flush()

    async def commit(self):
        await self.db.commit()

    async def update_user(self, user: User, user_data: dict) -> User:
        for field, value in user_data.items():
            setattr(user, field, value)

        self.db.add(user)
        return user

    async def soft_delete_user(self, user: User) -> None:
        user.is_active = False

    # token methods
    async def add_token_to_blacklist(self, token: str, expires_at: datetime) -> None:
        blacklisted_token = TokenBlacklist(
            token=token,
            expires_at=expires_at,
        )
        self.db.add(blacklisted_token)

    async def is_token_blacklisted(self, token: str) -> bool:
        query = (
            select(TokenBlacklist)
            .where(TokenBlacklist.token == token)
        )
        blacklisted = (await self.db.execute(query)).scalar_one_or_none()
        return blacklisted is not None
