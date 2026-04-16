from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.topics.models import (
    Entity,
    SavedTopic,
    SourceDocument,
    TimelineEvent,
    Topic,
    TopicEntity,
)


async def seed_minimal_data(session: AsyncSession) -> None:
    existing = await session.scalar(select(Topic.id).limit(1))
    if existing:
        return

    now = datetime.now(timezone.utc)

    topic = Topic(
        id="topic_20260414_001",
        slug="us-tariff-policy-shift",
        title="US Tariff Policy Shift Triggers Global Supply Chain Debate",
        title_zh="美国关税政策转向引发全球供应链大讨论",
        summary="Recent policy changes triggered renewed discussion across trade, manufacturing, and inflation topics.",
        summary_zh="近期政策变化引发了贸易、制造业和通胀相关话题的新一轮讨论。",
        region="international",
        category="economy",
        heat_score=87,
        freshness="rising",
        source_count=1,
        updated_at=now,
    )
    session.add(topic)

    entity = Entity(name="US Trade Office", entity_type="org")
    session.add(entity)
    await session.flush()

    session.add(TopicEntity(topic_id=topic.id, entity_id=entity.id, mention_count=2))
    session.add(
        TimelineEvent(
            topic_id=topic.id,
            title="Official statement released",
            title_zh="官方声明发布",
            timestamp=now,
            source="Gov Briefing",
        )
    )
    session.add(
        SourceDocument(
            topic_id=topic.id,
            title="Tariff shift and global trade",
            publisher="Example News",
            publish_time=now,
            url="https://example.com/tariff-shift",
            snippet="Policy shift may reshape sourcing decisions and inflation expectations.",
        )
    )

    # Keep table warm and schema verified even before save action.
    session.add(SavedTopic(topic_id=topic.id))
    await session.flush()
    await session.delete(await session.get(SavedTopic, topic.id))

    await session.commit()
