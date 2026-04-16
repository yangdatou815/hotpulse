"""Tests for /api/v1/saved endpoints.

Covers PRD requirements:
  - UC7: Bookmark/save important topics
  - Section 9 Feature 6: Save Topics
  - Section 16: Saved endpoints (GET/POST/DELETE)
"""
import pytest


async def test_saved_empty(client):
    """Initially no saved topics."""
    resp = await client.get("/api/v1/saved")
    assert resp.status_code == 200
    assert resp.json() == []


async def test_save_and_list(client, seed_topic):
    """PRD UC7: save a topic then retrieve saved list."""
    # Save
    resp = await client.post("/api/v1/saved", json={"topic_id": "topic_20260414_001"})
    assert resp.status_code == 201
    assert resp.json()["status"] == "saved"

    # List
    resp = await client.get("/api/v1/saved")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 1
    assert body[0]["id"] == "topic_20260414_001"


async def test_save_topic_not_found(client):
    """Saving a non-existent topic returns 404."""
    resp = await client.post("/api/v1/saved", json={"topic_id": "nonexistent"})
    assert resp.status_code == 404
    body = resp.json()
    assert body["detail"]["error"]["code"] == "TOPIC_NOT_FOUND"


async def test_save_idempotent(client, seed_topic):
    """Saving same topic twice should not fail or create duplicates."""
    await client.post("/api/v1/saved", json={"topic_id": "topic_20260414_001"})
    resp = await client.post("/api/v1/saved", json={"topic_id": "topic_20260414_001"})
    assert resp.status_code == 201

    body = (await client.get("/api/v1/saved")).json()
    assert len(body) == 1


async def test_delete_saved(client, seed_topic):
    """PRD Section 16: DELETE /saved/{topic_id}."""
    await client.post("/api/v1/saved", json={"topic_id": "topic_20260414_001"})
    resp = await client.delete("/api/v1/saved/topic_20260414_001")
    assert resp.status_code == 204

    # Should be empty now
    body = (await client.get("/api/v1/saved")).json()
    assert body == []


async def test_delete_nonexistent_saved_is_ok(client):
    """Deleting a non-saved topic should not error (idempotent)."""
    resp = await client.delete("/api/v1/saved/nonexistent")
    assert resp.status_code == 204
