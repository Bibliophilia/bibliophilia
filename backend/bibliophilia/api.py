from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Depends

from backend.bibliophilia.core.dependencies import get_session
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

from backend.bibliophilia.config import MIDDLEWARE_SECRET_KEY
from backend.bibliophilia.core.dependencies import engine
from backend.bibliophilia.core.models import BPModel

import backend.bibliophilia.books.api as books_api
import backend.bibliophilia.users.api as users_api
from starlette.types import Scope, ASGIApp


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    BPModel.metadata.create_all(engine)
    yield


bibliophilia_app = FastAPI(title="Bibliophilia API", version="1.0.0", lifespan=lifespan)
origins = [
    "http://localhost:3000",
    "http://localhost:3000",
    "http://elasticsearch:9200",
    "http://postgres:5432",
    "http://frontend:3000"
]

bibliophilia_app.add_middleware(SessionMiddleware, secret_key=MIDDLEWARE_SECRET_KEY)

bibliophilia_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins,
)

bibliophilia_app.include_router(books_api.router,
                                prefix="/books",
                                tags=["books"],
                                dependencies=[Depends(get_session)])

bibliophilia_app.include_router(users_api.router,
                                prefix="/users",
                                tags=["users"],
                                dependencies=[Depends(get_session)])


@bibliophilia_app.get("/health")
def health() -> str:
    return "Server is running!"
