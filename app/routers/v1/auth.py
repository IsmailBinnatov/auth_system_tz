from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.schemas.auth import UserRegister, UserResponse, UserLogin, UserUpdate, TokenResponse
from app.services.user import UserService
from app.models.models import User
from app.core.dependencies import get_user_service
from app.core.auth.dependencies import get_current_user, security


router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def user_register(
    user_data: UserRegister,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.user_register(user_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Registration failed',
        )
    return user


@router.post('/login', response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def user_login(
    user_data: UserLogin,
    user_service: UserService = Depends(get_user_service),
):
    token = await user_service.user_login(user_data.email, user_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Wrong credentials',
        )

    return TokenResponse(
        access_token=token,
        token_type='bearer',
    )


@router.get('/me', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.patch('/me', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.update_user(current_user, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Update failed',
        )
    return user


@router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    await user_service.soft_delete_user(current_user)


@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(
    current_user: User = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service),
):
    token = credentials.credentials
    await user_service.logout_user(token)
