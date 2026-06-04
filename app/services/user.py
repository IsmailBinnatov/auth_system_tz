from app.models.models import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(
            self,
            user_repo: UserRepository,
    ):
        self.user_repo = user_repo

    async def get_active_user_by_id(self, user_id: int) -> User | None:
        user = await self.user_repo.get_user_by_id(user_id)
        return user
