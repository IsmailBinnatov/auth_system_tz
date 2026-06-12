from fastapi import FastAPI

from app.routers.v1.auth import router as auth_router
from app.routers.v1.orders import router as orders_router
from app.routers.v1.products import router as product_router
from app.routers.v1.reports import router as reports_router


app = FastAPI(
    title='Auth Service',
    description='Authorization service',
    version='1.0.0',
)


app.include_router(auth_router)
app.include_router(orders_router)
app.include_router(product_router)
app.include_router(reports_router)


@app.get('/')
async def root():
    return {'message': 'The Auth Service is operating normally'}
