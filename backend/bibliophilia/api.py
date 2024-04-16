from contextlib import asynccontextmanager
from typing import AsyncIterator, Annotated
import json

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

# from backend.bibliophilia.server.dependencies import get_session, engine
from backend.bibliophilia.server.domain.models import BPModel

# from backend.bibliophilia.server.main import oauth
from starlette.responses import RedirectResponse

from backend.bibliophilia.server.settings import CLIENT_ID, CLIENT_SECRET

# from . import books, auth


# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncIterator[None]:
#    BPModel.metadata.create_all(engine)
#    yield


bibliophilia_app = FastAPI(title="Bibliophilia API", version="1.0.0")  # lifespan=lifespan
# bibliophilia_app.include_router(books.router,
#                                prefix="/books",
#                                tags=["books"],
#                                dependencies=[Depends(get_session)])


bibliophilia_app.add_middleware(SessionMiddleware, secret_key="bibliophilia")

bibliophilia_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432"],
    allow_credentials=True,
    allow_methods=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432"],
    allow_headers=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432"],
)

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': 'http://localhost:8000/auth'
    }
)

'''
bibliophilia_app.include_router(auth.router,
                                prefix="/"
                                tags=["auth"],
bibliophilia_app = FastAPI(title="Bibliophilia API", version="1.0.0", lifespan=lifespan)
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


@bibliophilia_app.get('/login')
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)


@bibliophilia_app.get('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return "Error"
    user = access_token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/get-user')


@bibliophilia_app.get('/logout')
async def logout(request: Request):
    request.session.pop('user')
    request.session.clear()
    return RedirectResponse(url='/health')


@bibliophilia_app.get('/get-user')
async def get_user(request: Request):
    user = request.session.get('user')
    if user is None:
        return RedirectResponse(url='/login')
    user_data = json.dumps(user, ensure_ascii=False)
    return {'user': user_data}

