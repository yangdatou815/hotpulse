"""API endpoint to trigger ingestion manually."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.ingestion.pipeline import run_pipeline

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


@router.post("/run")
async def trigger_ingestion(db: AsyncSession = Depends(get_db)) -> dict:
    stats = await run_pipeline(db)
    return {"status": "completed", **stats}
