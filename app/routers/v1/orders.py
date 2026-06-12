from fastapi import APIRouter, Depends, status

from app.core.auth.permissions import PermissionChecker


router = APIRouter(
    prefix='/orders',
    tags=['Orders'],
)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_orders(
    _permissions_checker: None = Depends(
        PermissionChecker('orders:read')
    ),
):
    return {'message': 'Orders list'}


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_orders(
    _permissions_checker: None = Depends(
        PermissionChecker('orders:create')
    ),
):
    return {'message': 'Order created'}


@router.patch('/{order_id}', status_code=status.HTTP_200_OK)
async def update_orders(
    order_id: int,
    _permissions_checker: None = Depends(
        PermissionChecker('orders:update')
    ),
):
    return {'message': f'Order {order_id} updated'}


@router.delete('/{order_id}', status_code=status.HTTP_200_OK)
async def delete_orders(
    order_id: int,
    _permissions_checker: None = Depends(
        PermissionChecker('orders:delete')
    ),
):
    return {'message': f'Order {order_id} deleted'}
