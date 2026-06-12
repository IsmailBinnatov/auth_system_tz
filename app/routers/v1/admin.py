from fastapi import APIRouter, Depends, status

from app.services.user import UserService
from app.core.dependencies import get_user_service
from app.core.auth.permissions import PermissionChecker


router = APIRouter(
    prefix='/admin',
    tags=['Admin API'],
)


@router.get('/users/{user_id}/permissions', status_code=status.HTTP_200_OK)
async def get_user_permissions(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    _permission_checker: None = Depends(
        PermissionChecker('users:delete')
    ),
):
    permissions = await user_service.get_user_permissions(user_id)
    return {'permissions': permissions}


@router.get('/users/{user_id}/roles', status_code=status.HTTP_200_OK)
async def get_user_permissions(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    _permission_checker: None = Depends(
        PermissionChecker('users:delete')
    ),
):
    roles = await user_service.get_user_roles(user_id)
    return {'roles': roles}


@router.post('/users/{user_id}/roles/{role_name}', status_code=status.HTTP_201_CREATED)
async def assign_role_to_user(
    user_id: int,
    role_name: str,
    user_service: UserService = Depends(get_user_service),
    _permission_checker: None = Depends(
        PermissionChecker('users:delete')
    ),
):
    await user_service.assign_role_to_user(user_id, role_name)
    return {'message': f'Role {role_name} assigned to user {user_id}'}


@router.delete('/users/{user_id}/roles/{role_name}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_role_from_user(
    user_id: int,
    role_name: str,
    user_service: UserService = Depends(get_user_service),
    _permission_checker: None = Depends(
        PermissionChecker('users:delete')
    ),
):
    await user_service.remove_role_from_user(user_id, role_name)
