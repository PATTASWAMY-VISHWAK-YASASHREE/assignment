from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import datasets, pipeline
from app.core.config import settings
from app.core.security import get_api_key


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(datasets.router, prefix="/api", dependencies=[Depends(get_api_key)])
    app.include_router(pipeline.router, prefix="/api", dependencies=[Depends(get_api_key)])

    @app.get("/api/health")
    async def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
