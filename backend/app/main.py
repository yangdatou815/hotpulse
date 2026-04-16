from __future__ import annotations

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.base import Base
from app.db.seed import seed_minimal_data
from app.db.session import SessionLocal, engine
from app.modules.saved.router import router as saved_router
from app.modules.search.router import router as search_router
from app.modules.topics.router import router as topics_router
from app.modules.ingestion.router import router as ingestion_router
from app.modules.topics import models as _topic_models  # noqa: F401

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
async def startup_event() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:  # type: AsyncSession
        await seed_minimal_data(session)


@app.get(f"{settings.api_prefix}/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(topics_router, prefix=settings.api_prefix)
app.include_router(search_router, prefix=settings.api_prefix)
app.include_router(saved_router, prefix=settings.api_prefix)
app.include_router(ingestion_router, prefix=settings.api_prefix)
