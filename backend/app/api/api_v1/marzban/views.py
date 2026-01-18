from fastapi import APIRouter
from marzban import UserResponse

from core.config import settings
from .crud import marzban_client
from .schemas import *

router = APIRouter(
    prefix=settings.api.v1.marzban,
    tags=["Marzban"]
)

@router.get('')
async def get_server_status():
    server_status = await marzban_client.get_server_status()
    return server_status


@router.get('/{username}', response_model=UserResponse)
async def get_user_info(username: str):
    sub_info = await marzban_client.get_user_info(username=username)
    return  sub_info


@router.post('/create-user', response_model=UserResponse)
async def create_user(data: CreateUser):
    response = await marzban_client.create_user(data=data)
    return response


@router.get('/reset_user/{username}', response_model=UserResponse)
async def reset_user(username: str):
    response = await marzban_client.reset_user(username=username)
    return response