from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Depends

from bibliophilia.core.dependencies import get_session, engine
from bibliophilia.core.models import BPModel

import bibliophilia.books.api as books_api


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    BPModel.metadata.create_all(engine)
    yield


bibliophilia_app = FastAPI(title="Bibliophilia API", version="1.0.0", lifespan=lifespan)
bibliophilia_app.include_router(books_api.router,
                                prefix="/books",
                                tags=["books"],
                                dependencies=[Depends(get_session)])


@bibliophilia_app.get("/health")
def health() -> str:
    return "Server is running!"
