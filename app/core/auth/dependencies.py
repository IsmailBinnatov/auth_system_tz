from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.auth.jwt import decode_token
from app.services.user import UserService
from app.core.dependencies import get_user_service


security = HTTPBearer()


def error_401_unautorized(msg: str = 'Could not validate credentials'):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=msg,
    )


async def get_current_user(
        user_service: UserService = Depends(get_user_service),
        credentials: HTTPAuthorizationCredentials = Depends(security),
):
    payload_dict = decode_token(credentials.credentials)

    if not payload_dict:
        error_401_unautorized()

    user_id = int(payload_dict['sub'])
    user = await user_service.get_active_user_by_id(user_id)

    if not user:
        error_401_unautorized()

    return user
