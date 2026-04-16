"""Shared test fixtures for HotPulse backend tests.

Uses an in-memory SQLite database so tests run without PostgreSQL.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.modules.topics.models import (
    Entity,
    SavedTopic,
    SourceDocument,
    TimelineEvent,
    Topic,
    TopicEntity,
)

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DB_URL, future=True)
TestSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
async def setup_db():
    """Create all tables before each test and drop after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


NOW = datetime(2026, 4, 14, 9, 30, 0, tzinfo=timezone.utc)


@pytest.fixture
async def seed_topic(db: AsyncSession) -> Topic:
    """Insert one topic with timeline, entity, and source."""
    topic = Topic(
        id="topic_20260414_001",
        slug="us-tariff-policy-shift",
        title="US Tariff Policy Shift Triggers Global Supply Chain Debate",
        summary="Recent policy changes triggered renewed discussion across trade, manufacturing, and inflation topics.",
        region="international",
        category="economy",
        heat_score=87,
        freshness="rising",
        source_count=1,
        updated_at=NOW,
    )
    db.add(topic)

    entity = Entity(name="US Trade Office", entity_type="org")
    db.add(entity)
    await db.flush()

    db.add(TopicEntity(topic_id=topic.id, entity_id=entity.id, mention_count=2))
    db.add(
        TimelineEvent(
            topic_id=topic.id,
            title="Official statement released",
            timestamp=NOW,
            source="Gov Briefing",
        )
    )
    db.add(
        SourceDocument(
            topic_id=topic.id,
            title="Tariff shift and global trade",
            publisher="Example News",
            publish_time=NOW,
            url="https://example.com/tariff-shift",
            snippet="Policy shift may reshape sourcing decisions and inflation expectations.",
        )
    )
    await db.commit()
    return topic


@pytest.fixture
async def seed_multiple_topics(db: AsyncSession) -> list[Topic]:
    """Insert multiple topics for list/filter/search tests."""
    topics_data = [
        {
            "id": "topic_dom_001",
            "slug": "domestic-ai-regulation",
            "title": "Domestic AI Regulation Framework Draft Released",
            "summary": "Government releases draft framework for AI regulation in domestic markets.",
            "region": "domestic",
            "category": "technology",
            "heat_score": 92,
            "freshness": "rising",
            "source_count": 5,
        },
        {
            "id": "topic_intl_001",
            "slug": "us-tariff-policy-shift",
            "title": "US Tariff Policy Shift Triggers Global Supply Chain Debate",
            "summary": "Recent policy changes triggered renewed discussion across trade.",
            "region": "international",
            "category": "economy",
            "heat_score": 87,
            "freshness": "rising",
            "source_count": 3,
        },
        {
            "id": "topic_dom_002",
            "slug": "cultural-heritage-protection",
            "title": "New Cultural Heritage Protection Act Passed",
            "summary": "Legislation to protect cultural heritage sites gains approval.",
            "region": "domestic",
            "category": "culture",
            "heat_score": 45,
            "freshness": "stable",
            "source_count": 2,
        },
        {
            "id": "topic_intl_002",
            "slug": "global-climate-summit",
            "title": "Global Climate Summit Opens with Bold Pledges",
            "summary": "Nations gather to discuss emission reductions and climate policy.",
            "region": "international",
            "category": "politics",
            "heat_score": 78,
            "freshness": "fading",
            "source_count": 8,
        },
    ]
    result = []
    for data in topics_data:
        t = Topic(updated_at=NOW, **data)
        db.add(t)
        result.append(t)
    await db.commit()
    return result
