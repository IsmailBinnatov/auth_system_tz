from fastapi import Depends, HTTPException, status

from app.core.auth.dependencies import get_current_user
from app.core.dependencies import get_user_service
from app.models.models import User
from app.services.user import UserService


class PermissionChecker:

    def __init__(self, permission: str):
        self.permission = permission

    async def __call__(
        self,
        current_user: User = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service),
    ):
        permissions = await user_service.get_user_permissions(current_user.id)

        if self.permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Permission denied',
            )
