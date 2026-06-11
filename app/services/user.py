from fastapi import HTTPException

from app.models.models import User
from app.repositories.user import UserRepository
from app.schemas.auth import UserRegister, UserUpdate
from app.core.auth.security import hash_password, verify_password
from app.core.auth.jwt import create_access_token


class UserService:
    def __init__(
            self,
            user_repo: UserRepository,
    ):
        self.user_repo = user_repo

    async def get_active_user_by_id(self, user_id: int) -> User | None:
        user = await self.user_repo.get_active_user_by_id(user_id)
        return user

    async def user_register(self, user_data: UserRegister) -> User | None:
        if not user_data.password == user_data.password_repeat:
            raise HTTPException(
                status_code=400, detail='Passwords do not match')

        email_exists = await self.user_repo.get_active_user_by_email(user_data.email)
        if email_exists:
            raise HTTPException(status_code=409, detail='Email exists')

        hashed_pswd = hash_password(user_data.password)

        new_user = User(
            name=user_data.name,
            surname=user_data.surname,
            middle_name=user_data.middle_name,
            email=user_data.email,
            hashed_password=hashed_pswd,
        )

        db_user = await self.user_repo.create_user(new_user)
        await self.user_repo.flush()

        await self.user_repo.assign_role_to_user(
            user_id=db_user.id,
            role_name='user',
        )

        await self.user_repo.commit()
        return db_user

    async def user_login(self, email: str, password: str) -> str | None:
        user = await self.user_repo.get_active_user_by_email(email)
        if not user:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        payload = {'sub': str(user.id)}
        token = create_access_token(payload)
        return token

    async def update_user(self, user: User, user_data: UserUpdate) -> User | None:
        updates = user_data.model_dump(exclude_unset=True)
        if not updates:
            return user

        new_email = updates.get('email')
        if new_email and new_email != user.email:
            email_exists = await self.user_repo.get_active_user_by_email(new_email)
            if email_exists:
                return None

        updated_user = await self.user_repo.update_user(user, updates)
        await self.user_repo.commit()
        return updated_user

    async def soft_delete_user(self, user: User) -> None:
        await self.user_repo.soft_delete_user(user)
        await self.user_repo.commit()
