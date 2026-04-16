from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    title: Mapped[str] = mapped_column(Text)
    title_zh: Mapped[str] = mapped_column(Text, default="")
    summary: Mapped[str] = mapped_column(Text)
    summary_zh: Mapped[str] = mapped_column(Text, default="")
    region: Mapped[str] = mapped_column(String(32), index=True)
    category: Mapped[str] = mapped_column(String(32), index=True)
    heat_score: Mapped[int] = mapped_column(Integer, default=0)
    freshness: Mapped[str] = mapped_column(String(16), default="stable")
    source_count: Mapped[int] = mapped_column(Integer, default=0)
    tags: Mapped[str] = mapped_column(Text, default="")  # comma-separated tags
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topic_id: Mapped[str] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(Text)
    title_zh: Mapped[str] = mapped_column(Text, default="")
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    source: Mapped[str] = mapped_column(String(255))


class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    entity_type: Mapped[str] = mapped_column(String(32))


class TopicEntity(Base):
    __tablename__ = "topic_entities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topic_id: Mapped[str] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), index=True)
    entity_id: Mapped[int] = mapped_column(ForeignKey("entities.id", ondelete="CASCADE"), index=True)
    mention_count: Mapped[int] = mapped_column(Integer, default=1)


class SourceDocument(Base):
    __tablename__ = "source_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    topic_id: Mapped[str] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(Text)
    publisher: Mapped[str] = mapped_column(String(255))
    publish_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    url: Mapped[str] = mapped_column(Text)
    snippet: Mapped[str] = mapped_column(Text)


class SavedTopic(Base):
    __tablename__ = "saved_topics"

    topic_id: Mapped[str] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True)
    saved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
