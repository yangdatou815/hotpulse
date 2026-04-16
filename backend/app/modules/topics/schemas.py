from datetime import datetime
from typing import Literal

from pydantic import BaseModel


Region = Literal["domestic", "international"]
Category = Literal["politics", "economy", "technology", "society", "business", "culture"]
Freshness = Literal["rising", "stable", "fading"]


class TopicSummary(BaseModel):
    id: str
    slug: str
    title: str
    summary: str
    region: Region
    category: Category
    heat_score: int
    freshness: Freshness
    source_count: int
    tags: list[str]
    updated_at: datetime


class TimelineItem(BaseModel):
    title: str
    timestamp: datetime
    source: str


class EntityItem(BaseModel):
    name: str
    entity_type: Literal["person", "org", "location"]


class SourceItem(BaseModel):
    title: str
    publisher: str
    publish_time: datetime
    url: str
    snippet: str


class TopicDetail(TopicSummary):
    timeline: list[TimelineItem]
    entities: list[EntityItem]
    sources: list[SourceItem]


class PaginatedTopics(BaseModel):
    items: list[TopicSummary]
    total: int
    page: int
    size: int
