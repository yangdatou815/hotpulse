"""Pipeline orchestrator: fetch → cluster → extract → persist.

This module ties together all ingestion steps and writes results
to the database via SQLAlchemy.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ingestion.clustering import TopicCluster, cluster_articles
from app.modules.ingestion.entities import extract_entities
from app.modules.ingestion.fetcher import FeedSource, RawArticle, fetch_articles
from app.modules.topics.models import (
    Entity,
    SourceDocument,
    TimelineEvent,
    Topic,
    TopicEntity,
)


def _make_slug(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s]+", "-", slug.strip())
    return slug[:120]


async def run_pipeline(
    session: AsyncSession,
    sources: list[FeedSource] | None = None,
) -> dict[str, int]:
    """Execute the full ingestion pipeline.

    Returns a summary dict: {articles_fetched, topics_created, topics_updated}.
    """
    stats = {"articles_fetched": 0, "topics_created": 0, "topics_updated": 0}

    # 1. Fetch
    articles = await fetch_articles(sources)
    stats["articles_fetched"] = len(articles)
    if not articles:
        return stats

    # 2. Cluster
    clusters = cluster_articles(articles)

    # 3. For each cluster: persist topic + sources + timeline + entities
    for cluster in clusters:
        slug = _make_slug(cluster.title)

        # Check if topic already exists (by slug)
        existing = await session.scalar(
            select(Topic).where(Topic.slug == slug).limit(1)
        )
        now = datetime.now(timezone.utc)

        if existing:
            # Update existing topic
            existing.heat_score = max(existing.heat_score, cluster.heat_score)
            existing.freshness = cluster.freshness
            existing.source_count = existing.source_count + len(cluster.articles)
            existing.updated_at = now
            topic = existing
            stats["topics_updated"] += 1
        else:
            # Create new topic
            topic = Topic(
                id=cluster.cluster_id,
                slug=slug,
                title=cluster.title,
                summary=cluster.summary,
                region=cluster.region,
                category=cluster.category,
                heat_score=cluster.heat_score,
                freshness=cluster.freshness,
                source_count=len(cluster.articles),
                updated_at=now,
            )
            session.add(topic)
            await session.flush()
            stats["topics_created"] += 1

        # Add source documents (dedupe by URL)
        existing_urls_result = await session.scalars(
            select(SourceDocument.url).where(SourceDocument.topic_id == topic.id)
        )
        existing_urls = set(existing_urls_result.all())

        for article in cluster.articles:
            if article.url not in existing_urls:
                session.add(
                    SourceDocument(
                        topic_id=topic.id,
                        title=article.title,
                        publisher=article.publisher,
                        publish_time=article.publish_time,
                        url=article.url,
                        snippet=article.snippet[:500] if article.snippet else "",
                    )
                )
                existing_urls.add(article.url)

        # Generate timeline events from articles
        existing_timeline = await session.scalars(
            select(TimelineEvent.title).where(TimelineEvent.topic_id == topic.id)
        )
        existing_tl_titles = set(existing_timeline.all())

        # Pick up to 5 most notable articles as timeline milestones
        sorted_articles = sorted(cluster.articles, key=lambda a: a.publish_time)
        for article in sorted_articles[:5]:
            tl_title = article.title[:200]
            if tl_title not in existing_tl_titles:
                session.add(
                    TimelineEvent(
                        topic_id=topic.id,
                        title=tl_title,
                        timestamp=article.publish_time,
                        source=article.publisher,
                    )
                )
                existing_tl_titles.add(tl_title)

        # Extract and persist entities
        texts = [a.raw_text for a in cluster.articles]
        extracted = extract_entities(texts)

        for ent in extracted:
            # Find or create entity
            db_entity = await session.scalar(
                select(Entity).where(
                    Entity.name == ent.name,
                    Entity.entity_type == ent.entity_type,
                ).limit(1)
            )
            if not db_entity:
                db_entity = Entity(name=ent.name, entity_type=ent.entity_type)
                session.add(db_entity)
                await session.flush()

            # Link to topic
            existing_link = await session.scalar(
                select(TopicEntity).where(
                    TopicEntity.topic_id == topic.id,
                    TopicEntity.entity_id == db_entity.id,
                ).limit(1)
            )
            if existing_link:
                existing_link.mention_count = max(existing_link.mention_count, ent.count)
            else:
                session.add(
                    TopicEntity(
                        topic_id=topic.id,
                        entity_id=db_entity.id,
                        mention_count=ent.count,
                    )
                )

    await session.commit()
    return stats
