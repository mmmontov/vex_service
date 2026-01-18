from fastapi import APIRouter

from core.config import settings
from .blitz.views import router as blitz_router
from .marzban.views import router as marzban_router

router = APIRouter(
    prefix=settings.api.v1.prefix
)


router.include_router(
    blitz_router
)

router.include_router(
    marzban_router
)