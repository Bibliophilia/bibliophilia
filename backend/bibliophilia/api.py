import os

from fastapi import FastAPI, Depends

#from backend.bibliophilia.core.dependencies import get_session

import backend.bibliophilia.users.api.google_auth as google_auth_api
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

load_dotenv()



#@asynccontextmanager
#async def lifespan(app: FastAPI) -> AsyncIterator[None]:
#    BPModel.metadata.create_all(engine)
#    yield


bibliophilia_app = FastAPI(title="Bibliophilia API", version="1.0.0")  #lifespan=lifespan

bibliophilia_app.add_middleware(SessionMiddleware, secret_key=os.environ.get("MIDDLEWARE_SECRET_KEY"))


bibliophilia_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432", "http://frontend:3000"],
    allow_headers=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432", "http://frontend:3000"],
)

'''
bibliophilia_app.include_router(books_api.router,
                                prefix="/books",
                                tags=["books"],
                                dependencies=[Depends(get_session)])
'''

bibliophilia_app.include_router(google_auth_api.router,
                                #prefix="/",
                                tags=["auth"])
                                #dependencies=[Depends(get_session)])

'''
bibliophilia_app.include_router(review_api.router,
                                prefix="/review",
                                tags=["review"],
                                dependencies=[Depends(get_session)])
'''

@bibliophilia_app.get("/health")
def health() -> str:
    return "Server is running!"

