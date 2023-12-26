from fastapi import FastAPI

from bibliophilia.server.view.api.routes.api import bibliophilia_app
from fastapi.middleware.cors import CORSMiddleware


def get_application() -> FastAPI:
    return bibliophilia_app


app = get_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432", "http://frontend:3000"],
    allow_headers=["http://localhost:3000", "http://elasticsearch:9200", "http://postgres:5432", "http://frontend:3000"],
)
