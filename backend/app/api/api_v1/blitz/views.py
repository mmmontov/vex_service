from fastapi import APIRouter

from core.config import settings
from .crud import blitz_client
from .schemas import *

router = APIRouter(
    prefix=settings.api.v1.blitz,
    tags=["Blitz panel"]
)

@router.get('')
async def get_server_status():
    server_status = await blitz_client.get_server_status()
    return server_status


@router.get('/{username}', response_model=UserInfo)
async def get_user_info(username: str):
    user_info = await blitz_client.get_user_info(username=username)
    return user_info


@router.post('/create-user', response_model=ApiResponse)
async def create_user(data: CreateUser):
    response = await blitz_client.create_user(data=data)
    return response


@router.get('/reset_user/{username}', response_model=ApiResponse)
async def reset_user(username: str):
    response = await blitz_client.reset_user(username=username)
    return response