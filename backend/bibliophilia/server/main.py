from fastapi import FastAPI

from bibliophilia.server.view.api.routes.api import bibliophilia_app


def get_application() -> FastAPI:
    return bibliophilia_app


app = get_application()
