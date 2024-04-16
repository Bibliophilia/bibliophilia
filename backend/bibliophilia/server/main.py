from fastapi import FastAPI

from backend.bibliophilia.server.view.api.routes.api import bibliophilia_app
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
from settings import CLIENT_ID, CLIENT_SECRET


def get_application() -> FastAPI:
    return bibliophilia_app


'''
app = get_application()

app.add_middleware(SessionMiddleware, secret_key="bibliophilia")

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
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432"],
    allow_credentials=True,
    allow_methods=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432"],
    allow_headers=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432"],
)
"""
