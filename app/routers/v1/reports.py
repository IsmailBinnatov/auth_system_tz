from fastapi import APIRouter, Depends, status

from app.core.auth.permissions import PermissionChecker


router = APIRouter(
    prefix='/reports',
    tags=['Reports'],
)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_reports(
    _permissions_checker: None = Depends(
        PermissionChecker('reports:read')
    ),
):
    return {'message': 'Reports list'}


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_reports(
    _permissions_checker: None = Depends(
        PermissionChecker('reports:create')
    ),
):
    return {'message': 'Report created'}
