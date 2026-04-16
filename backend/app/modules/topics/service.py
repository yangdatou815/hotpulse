from __future__ import annotations

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.topics.models import Entity, SavedTopic, SourceDocument, TimelineEvent, Topic, TopicEntity
from app.modules.topics.schemas import EntityItem, PaginatedTopics, SourceItem, TimelineItem, TopicDetail, TopicSummary


def _summary_from_model(topic: Topic, lang: str = "en") -> TopicSummary:
    tags = [t.strip() for t in (topic.tags or "").split(",") if t.strip()]
    title = (topic.title_zh if lang == "zh" and topic.title_zh else topic.title)
    summary = (topic.summary_zh if lang == "zh" and topic.summary_zh else topic.summary)
    return TopicSummary(
        id=topic.id,
        slug=topic.slug,
        title=title,
        summary=summary,
        region=topic.region,
        category=topic.category,
        heat_score=topic.heat_score,
        freshness=topic.freshness,
        source_count=topic.source_count,
        tags=tags,
        updated_at=topic.updated_at,
    )


async def list_topics(
    db: AsyncSession,
    region: str | None,
    category: str | None,
    q: str | None,
    tag: str | None,
    page: int,
    size: int,
    lang: str = "en",
) -> PaginatedTopics:
    filters = []
    if region:
        filters.append(Topic.region == region)
    if category:
        filters.append(Topic.category == category)
    if q:
        like_q = f"%{q.lower()}%"
        filters.append(or_(func.lower(Topic.title).like(like_q), func.lower(Topic.summary).like(like_q)))
    if tag:
        like_tag = f"%{tag}%"
        filters.append(Topic.tags.like(like_tag))

    where_expr = and_(*filters) if filters else None

    count_stmt = select(func.count()).select_from(Topic)
    if where_expr is not None:
        count_stmt = count_stmt.where(where_expr)
    total = int((await db.scalar(count_stmt)) or 0)

    stmt = select(Topic)
    if where_expr is not None:
        stmt = stmt.where(where_expr)
    stmt = stmt.order_by(Topic.heat_score.desc()).offset((page - 1) * size).limit(size)

    rows = (await db.scalars(stmt)).all()
    return PaginatedTopics(items=[_summary_from_model(t, lang) for t in rows], total=total, page=page, size=size)


async def get_topic_detail(db: AsyncSession, slug: str, lang: str = "en") -> TopicDetail | None:
    topic = await db.scalar(select(Topic).where(Topic.slug == slug).limit(1))
    if not topic:
        return None

    timeline_rows = (
        await db.scalars(select(TimelineEvent).where(TimelineEvent.topic_id == topic.id).order_by(TimelineEvent.timestamp.asc()))
    ).all()
    source_rows = (
        await db.scalars(select(SourceDocument).where(SourceDocument.topic_id == topic.id).order_by(SourceDocument.publish_time.desc()))
    ).all()

    entity_rows = (
        await db.execute(
            select(Entity)
            .join(TopicEntity, TopicEntity.entity_id == Entity.id)
            .where(TopicEntity.topic_id == topic.id)
            .order_by(Entity.name.asc())
        )
    ).scalars().all()

    return TopicDetail(
        **_summary_from_model(topic, lang).model_dump(),
        timeline=[
            TimelineItem(
                title=(t.title_zh if lang == "zh" and t.title_zh else t.title),
                timestamp=t.timestamp,
                source=t.source,
            )
            for t in timeline_rows
        ],
        entities=[EntityItem(name=e.name, entity_type=e.entity_type) for e in entity_rows],
        sources=[
            SourceItem(
                title=s.title,
                publisher=s.publisher,
                publish_time=s.publish_time,
                url=s.url,
                snippet=s.snippet,
            )
            for s in source_rows
        ],
    )


async def search_topics(
    db: AsyncSession,
    q: str,
    region: str | None,
    category: str | None,
    tag: str | None,
    page: int,
    size: int,
    lang: str = "en",
) -> PaginatedTopics:
    return await list_topics(db=db, region=region, category=category, q=q, tag=tag, page=page, size=size, lang=lang)


async def list_saved_topics(db: AsyncSession, lang: str = "en") -> list[TopicSummary]:
    rows = (
        await db.execute(
            select(Topic)
            .join(SavedTopic, SavedTopic.topic_id == Topic.id)
            .order_by(SavedTopic.saved_at.desc())
        )
    ).scalars().all()
    return [_summary_from_model(t, lang) for t in rows]


async def save_topic(db: AsyncSession, topic_id: str) -> bool:
    topic = await db.get(Topic, topic_id)
    if not topic:
        return False

    saved = await db.get(SavedTopic, topic_id)
    if not saved:
        db.add(SavedTopic(topic_id=topic_id))
        await db.commit()
    return True


async def delete_saved_topic(db: AsyncSession, topic_id: str) -> None:
    saved = await db.get(SavedTopic, topic_id)
    if saved:
        await db.delete(saved)
        await db.commit()
