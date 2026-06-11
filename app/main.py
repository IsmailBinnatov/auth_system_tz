from fastapi import FastAPI

from app.routers.v1.auth import router as auth_router


app = FastAPI(
    title='Auth Service',
    description='Authorization service',
    version='1.0.0',
)


app.include_router(auth_router)


@app.get('/')
async def root():
    return {'message': 'The Auth Service is operating normally'}
