from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.topics.schemas import PaginatedTopics
from app.modules.topics.service import search_topics

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=PaginatedTopics)
async def search(
    q: str = Query(..., min_length=1, max_length=200),
    region: str | None = Query(default=None),
    category: str | None = Query(default=None),
    tag: str | None = Query(default=None, max_length=100),
    lang: str = Query(default="en", regex="^(en|zh)$"),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> PaginatedTopics:
    return await search_topics(db=db, q=q, region=region, category=category, tag=tag, page=page, size=size, lang=lang)
