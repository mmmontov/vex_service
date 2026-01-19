from fastapi import APIRouter

from core.config import settings, BlitzPanel, Marzban
from .blitz.views import router as blitz_router
from .marzban.views import router as marzban_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)


def check_env(config: BlitzPanel | Marzban):
    have_username = config.username != 'username'
    have_password = config.password != 'password'
    return have_username and have_password

if check_env(settings.blitz):
    router.include_router(blitz_router)


if check_env(settings.marzban):
    router.include_router(marzban_router)