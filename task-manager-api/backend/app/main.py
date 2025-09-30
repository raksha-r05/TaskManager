from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from .api.v1.api import api_router
from .core.config import get_settings
from .web.routes import router as web_router
from .core.database import engine, Base


BASE_DIR = Path(__file__).resolve().parent


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api/v1")
    app.include_router(web_router)

    app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
    templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
    # Simple ping
    @app.get("/ping")
    async def ping() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()


@app.on_event("startup")
async def on_startup() -> None:
    # Ensure tables exist (useful for SQLite/dev). In production, prefer Alembic migrations.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


