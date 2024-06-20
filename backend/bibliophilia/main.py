import os

from fastapi import FastAPI

from backend.bibliophilia.api import bibliophilia_app
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


def get_application() -> FastAPI:
    return bibliophilia_app


app = get_application()


app.add_middleware(SessionMiddleware, secret_key=os.environ.get("MIDDLEWARE_SECRET_KEY"))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432", "http://frontend:3000"],
    allow_headers=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432", "http://frontend:3000"],
)
