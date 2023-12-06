from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from bibliophilia.server.db.tables import BibilophiliaDB
from fastapi import FastAPI, Depends
from .dependencies import engine, get_session
from .routers import books


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    BibilophiliaDB.metadata.create_all(engine)
    yield


bibliophilia_app = FastAPI(title="Bibliophila API", version="1.0.0", lifespan=lifespan)
bibliophilia_app.include_router(books.router,
                                prefix="/books",
                                tags=["books"],
                                dependencies=[Depends(get_session)])

@bibliophilia_app.get("/health")
def health() -> str:
    return "Server is running!"
