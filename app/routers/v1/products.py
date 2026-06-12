from fastapi import APIRouter, Depends, status

from app.core.auth.permissions import PermissionChecker


router = APIRouter(
    prefix='/products',
    tags=['Products'],
)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_products(
    _permissions_checker: None = Depends(
        PermissionChecker('products:read')
    ),
):
    return {'message': 'Products list'}


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_products(
    _permissions_checker: None = Depends(
        PermissionChecker('products:create')
    ),
):
    return {'message': 'Product created'}


@router.patch('/{product_id}', status_code=status.HTTP_200_OK)
async def update_products(
    product_id: int,
    _permissions_checker: None = Depends(
        PermissionChecker('products:update')
    ),
):
    return {'message': f'Product {product_id} updated'}


@router.delete('/{product_id}', status_code=status.HTTP_200_OK)
async def delete_products(
    product_id: int,
    _permissions_checker: None = Depends(
        PermissionChecker('products:delete')
    ),
):
    return {'message': f'Product {product_id} deleted'}
