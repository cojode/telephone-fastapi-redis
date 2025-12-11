from fastapi import FastAPI

from src.api.router import api_router
from src.lifespan import lifespan_setup


def get_app() -> FastAPI:
    app = FastAPI(docs_url="/api/docs", lifespan=lifespan_setup)

    app.include_router(api_router)

    return app
