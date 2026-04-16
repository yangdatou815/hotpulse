"""Tests for /api/v1/search endpoint.

Covers PRD requirements:
  - UC6: Search for topic keyword
  - Section 10: Search Requirements
  - Section 16: GET /api/v1/search?q=...
"""
import pytest


async def test_search_requires_query(client):
    """q param is required (min_length=1)."""
    resp = await client.get("/api/v1/search")
    assert resp.status_code == 422  # validation error


async def test_search_returns_matching_topics(client, seed_multiple_topics):
    """PRD UC6: search by keyword returns matching topics."""
    resp = await client.get("/api/v1/search", params={"q": "climate"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == 1
    assert "climate" in body["items"][0]["title"].lower()


async def test_search_case_insensitive(client, seed_multiple_topics):
    """Search should be case-insensitive."""
    resp = await client.get("/api/v1/search", params={"q": "TARIFF"})
    body = resp.json()
    assert body["total"] == 1


async def test_search_matches_summary(client, seed_multiple_topics):
    """Search should match in summary text too."""
    resp = await client.get("/api/v1/search", params={"q": "emission"})
    body = resp.json()
    assert body["total"] == 1
    assert body["items"][0]["slug"] == "global-climate-summit"


async def test_search_no_results(client, seed_multiple_topics):
    resp = await client.get("/api/v1/search", params={"q": "zzzznotfound"})
    body = resp.json()
    assert body["total"] == 0
    assert body["items"] == []


async def test_search_with_region_filter(client, seed_multiple_topics):
    """PRD Section 10: search supports region filter."""
    resp = await client.get("/api/v1/search", params={"q": "regulation", "region": "domestic"})
    body = resp.json()
    assert body["total"] == 1
    assert body["items"][0]["region"] == "domestic"


async def test_search_with_category_filter(client, seed_multiple_topics):
    """PRD Section 10: search supports category filter."""
    resp = await client.get("/api/v1/search", params={"q": "policy", "category": "economy"})
    body = resp.json()
    assert body["total"] == 1
    assert body["items"][0]["category"] == "economy"


async def test_search_pagination(client, seed_multiple_topics):
    """Search should support pagination."""
    resp = await client.get("/api/v1/search", params={"q": "a", "size": 2, "page": 1})
    body = resp.json()
    assert body["size"] == 2
    assert body["page"] == 1
