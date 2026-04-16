from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.topics.schemas import PaginatedTopics, TopicDetail
from app.modules.topics.service import get_topic_detail, list_topics

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=PaginatedTopics)
async def get_topics(
    region: str | None = Query(default=None),
    category: str | None = Query(default=None),
    q: str | None = Query(default=None, max_length=200),
    tag: str | None = Query(default=None, max_length=100),
    lang: str = Query(default="en", regex="^(en|zh)$"),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> PaginatedTopics:
    return await list_topics(db=db, region=region, category=category, q=q, tag=tag, page=page, size=size, lang=lang)


@router.get("/{topic_slug}", response_model=TopicDetail)
async def get_topic(
    topic_slug: str,
    lang: str = Query(default="en", regex="^(en|zh)$"),
    db: AsyncSession = Depends(get_db),
) -> TopicDetail:
    topic = await get_topic_detail(db, topic_slug, lang=lang)
    if not topic:
        raise HTTPException(status_code=404, detail={"error": {"code": "TOPIC_NOT_FOUND", "message": f"Topic '{topic_slug}' not found", "details": {}}})
    return topic


@router.get("/{topic_slug}/timeline")
async def get_timeline(
    topic_slug: str,
    lang: str = Query(default="en", regex="^(en|zh)$"),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, str]]:
    topic = await get_topic_detail(db, topic_slug, lang=lang)
    if not topic:
        raise HTTPException(status_code=404, detail={"error": {"code": "TOPIC_NOT_FOUND", "message": f"Topic '{topic_slug}' not found", "details": {}}})
    return [item.model_dump(mode="json") for item in topic.timeline]


@router.get("/{topic_slug}/sources")
async def get_sources(
    topic_slug: str,
    lang: str = Query(default="en", regex="^(en|zh)$"),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, str]]:
    topic = await get_topic_detail(db, topic_slug, lang=lang)
    if not topic:
        raise HTTPException(status_code=404, detail={"error": {"code": "TOPIC_NOT_FOUND", "message": f"Topic '{topic_slug}' not found", "details": {}}})
    return [item.model_dump(mode="json") for item in topic.sources]
