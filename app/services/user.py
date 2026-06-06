from fastapi import HTTPException

from app.models.models import User
from app.repositories.user import UserRepository
from app.schemas.auth import UserRegister
from app.core.auth.security import hash_password


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

        email_exists = await self.user_repo.get_user_by_email(user_data.email)
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

        return db_user
