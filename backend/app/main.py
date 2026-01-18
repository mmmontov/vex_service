from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import router as api_router
from api.api_v1.blitz.crud import blitz_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    blitz_client.close()


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(api_router)
