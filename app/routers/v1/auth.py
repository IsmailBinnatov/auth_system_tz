from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.auth import UserRegister, UserResponse, UserLogin, TokenResponse
from app.services.user import UserService
from app.core.dependencies import get_user_service


router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/register', response_model=UserResponse)
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


@router.post('/login', response_model=TokenResponse)
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
