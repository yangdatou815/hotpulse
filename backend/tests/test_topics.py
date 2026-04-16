"""Tests for /api/v1/topics endpoints.

Covers PRD requirements:
  - UC1: See top hot topics
  - UC2: Open topic and view timeline
  - UC3: See key entities connected to a topic
  - UC4: Concise summary with supporting sources
  - UC5: Filter topics by category and geography
  - Section 10: Topic Feed & Detail functional requirements
  - Section 16: API spec for topics endpoints
"""
import pytest


# === Topic List (PRD UC1, UC5, Section 10 Topic Feed) ===

async def test_list_topics_empty(client):
    """Empty DB returns empty list with pagination."""
    resp = await client.get("/api/v1/topics")
    assert resp.status_code == 200
    body = resp.json()
    assert body["items"] == []
    assert body["total"] == 0
    assert body["page"] == 1


async def test_list_topics(client, seed_multiple_topics):
    """Returns all topics ordered by heat_score descending (PRD: rank by heat)."""
    resp = await client.get("/api/v1/topics")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == 4
    scores = [t["heat_score"] for t in body["items"]]
    assert scores == sorted(scores, reverse=True), "Topics must be sorted by heat_score DESC"


async def test_list_topics_response_shape(client, seed_multiple_topics):
    """Each topic item includes all PRD-required fields (Section 10)."""
    resp = await client.get("/api/v1/topics")
    body = resp.json()
    required_fields = {"id", "slug", "title", "summary", "heat_score", "freshness", "region", "category", "source_count", "updated_at"}
    for item in body["items"]:
        assert required_fields.issubset(item.keys()), f"Missing fields: {required_fields - item.keys()}"


async def test_filter_by_region_domestic(client, seed_multiple_topics):
    """PRD UC5: filter by geography / region=domestic."""
    resp = await client.get("/api/v1/topics", params={"region": "domestic"})
    body = resp.json()
    assert body["total"] == 2
    assert all(t["region"] == "domestic" for t in body["items"])


async def test_filter_by_region_international(client, seed_multiple_topics):
    """PRD UC5: filter by geography / region=international."""
    resp = await client.get("/api/v1/topics", params={"region": "international"})
    body = resp.json()
    assert body["total"] == 2
    assert all(t["region"] == "international" for t in body["items"])


async def test_filter_by_category(client, seed_multiple_topics):
    """PRD UC5: filter by category."""
    resp = await client.get("/api/v1/topics", params={"category": "economy"})
    body = resp.json()
    assert body["total"] == 1
    assert body["items"][0]["category"] == "economy"


async def test_filter_by_region_and_category(client, seed_multiple_topics):
    """Combined region + category filter."""
    resp = await client.get("/api/v1/topics", params={"region": "domestic", "category": "technology"})
    body = resp.json()
    assert body["total"] == 1
    assert body["items"][0]["slug"] == "domestic-ai-regulation"


async def test_keyword_filter_on_topics(client, seed_multiple_topics):
    """PRD UC6: search/q param on topic list."""
    resp = await client.get("/api/v1/topics", params={"q": "tariff"})
    body = resp.json()
    assert body["total"] == 1
    assert "tariff" in body["items"][0]["title"].lower()


async def test_pagination(client, seed_multiple_topics):
    """PRD Section 10: paginated list."""
    resp = await client.get("/api/v1/topics", params={"page": 1, "size": 2})
    body = resp.json()
    assert len(body["items"]) == 2
    assert body["total"] == 4
    assert body["page"] == 1
    assert body["size"] == 2

    resp2 = await client.get("/api/v1/topics", params={"page": 2, "size": 2})
    body2 = resp2.json()
    assert len(body2["items"]) == 2
    assert body2["page"] == 2

    # No overlap
    ids1 = {t["id"] for t in body["items"]}
    ids2 = {t["id"] for t in body2["items"]}
    assert ids1.isdisjoint(ids2)


async def test_pagination_beyond_total(client, seed_multiple_topics):
    resp = await client.get("/api/v1/topics", params={"page": 100, "size": 20})
    body = resp.json()
    assert body["items"] == []
    assert body["total"] == 4


# === Topic Detail (PRD UC2, UC3, UC4, Section 10 Topic Detail) ===

async def test_topic_detail(client, seed_topic):
    """PRD Section 10: topic detail returns summary, timeline, entities, sources."""
    resp = await client.get("/api/v1/topics/us-tariff-policy-shift")
    assert resp.status_code == 200
    body = resp.json()
    assert body["slug"] == "us-tariff-policy-shift"
    assert body["title"] == "US Tariff Policy Shift Triggers Global Supply Chain Debate"
    assert "summary" in body
    assert isinstance(body["timeline"], list)
    assert isinstance(body["entities"], list)
    assert isinstance(body["sources"], list)


async def test_topic_detail_timeline_shape(client, seed_topic):
    """PRD UC2: timeline with title, timestamp, source reference."""
    resp = await client.get("/api/v1/topics/us-tariff-policy-shift")
    body = resp.json()
    assert len(body["timeline"]) >= 1
    tl = body["timeline"][0]
    assert "title" in tl
    assert "timestamp" in tl
    assert "source" in tl


async def test_topic_detail_entities_shape(client, seed_topic):
    """PRD UC3: entities with name and entity_type."""
    resp = await client.get("/api/v1/topics/us-tariff-policy-shift")
    body = resp.json()
    assert len(body["entities"]) >= 1
    ent = body["entities"][0]
    assert ent["name"] == "US Trade Office"
    assert ent["entity_type"] == "org"


async def test_topic_detail_sources_shape(client, seed_topic):
    """PRD UC4: sources with title, publisher, publish_time, url, snippet."""
    resp = await client.get("/api/v1/topics/us-tariff-policy-shift")
    body = resp.json()
    assert len(body["sources"]) >= 1
    src = body["sources"][0]
    for field in ("title", "publisher", "publish_time", "url", "snippet"):
        assert field in src, f"Source missing field: {field}"


async def test_topic_detail_not_found(client):
    """404 with structured error when topic does not exist (PRD Section 16)."""
    resp = await client.get("/api/v1/topics/nonexistent-slug")
    assert resp.status_code == 404
    body = resp.json()
    assert "detail" in body
    assert body["detail"]["error"]["code"] == "TOPIC_NOT_FOUND"


# === Timeline sub-endpoint ===

async def test_timeline_endpoint(client, seed_topic):
    """PRD Section 16: GET /topics/{slug}/timeline."""
    resp = await client.get("/api/v1/topics/us-tariff-policy-shift/timeline")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) >= 1


async def test_timeline_not_found(client):
    resp = await client.get("/api/v1/topics/nope/timeline")
    assert resp.status_code == 404


# === Sources sub-endpoint ===

async def test_sources_endpoint(client, seed_topic):
    """PRD Section 16: GET /topics/{slug}/sources."""
    resp = await client.get("/api/v1/topics/us-tariff-policy-shift/sources")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) >= 1


async def test_sources_not_found(client):
    resp = await client.get("/api/v1/topics/nope/sources")
    assert resp.status_code == 404
