---
applyTo: "backend/tests/**,frontend/src/**/*.{test,spec}.{ts,tsx}"
---

# SCT Case Design from User Stories — HotPulse

## Overview

SCT (System Component Test) cases for HotPulse are derived from the **User Stories** in `PRD.md § 6`.
Each User Story defines an observable user goal. SCT cases verify that the system satisfies that goal
through concrete API + UI interactions with defined inputs and expected outputs.

---

## User Story → SCT Case Mapping Rule

Each User Story generates **at minimum**:
- 1 normal case (happy path, stated goal succeeds)
- 3 abnormal cases, chosen from: invalid input, unauthorized/forbidden path if applicable,
  empty/no-data state, dependency failure/degradation, boundary-value rejection
- N additional cases for each meaningful variant (filter combination, sorting, pagination boundary, etc.)

Minimum SCT count per changed US: 4 cases (1 normal + 3 abnormal).

---

## SCT Case File Format

Each case is a structured markdown block. Cases may live in:
- `backend/tests/integration/test_<feature>_sct.py` — API-layer SCT
- `frontend/src/features/<feature>/__tests__/<Feature>.sct.test.tsx` — UI-layer SCT

Use this header comment block inside test files to document the case spec:

```
# SCT-<US_ID>-<N>
# User Story: <exact US text>
# Scenario:   <what variant this case covers>
# Priority:   High | Medium | Low
# Layer:      API | UI | E2E
#
# Precondition:
#   - <system state required before the test>
#
# Input:
#   - <user action or API call with concrete parameters>
#
# Expected Output:
#   - <verifiable response, state, or UI element>
```

---

## User Story Coverage — HotPulse MVP

### US-1: View top hot topics

> As a user, I want to see the top hot topics now, so that I can identify the most important developments immediately.

| Case ID | Scenario | Layer | Priority |
|---------|----------|-------|----------|
| SCT-US1-1 | Topics list returns paginated results sorted by heat_score DESC | API | High |
| SCT-US1-2 | Response includes required fields: id, title, slug, summary, heat_score, freshness, region, category, source_count, updated_at | API | High |
| SCT-US1-3 | Empty database returns empty items list with total=0, not an error | API | Medium |
| SCT-US1-4 | Homepage renders topic cards with title, heat score, and freshness badge | UI | High |
| SCT-US1-5 | First page loads within 2.5 seconds (< 500ms API p95) | API | Medium |

**API test sketch (SCT-US1-1):**
```python
# SCT-US1-1
# User Story: see top hot topics now
# Scenario:   default list sorted by heat_score DESC
# Priority:   High
# Layer:      API
#
# Precondition:
#   - DB contains at least 3 topics with different heat_scores
#
# Input:
#   - GET /api/v1/topics
#
# Expected Output:
#   - 200 OK
#   - items[0].heat_score >= items[1].heat_score >= items[2].heat_score
#   - response contains: items, total, page, size

async def test_topics_sorted_by_heat_score(client, seed_topics):
    response = await client.get("/api/v1/topics")
    assert response.status_code == 200
    data = response.json()
    scores = [t["heat_score"] for t in data["items"]]
    assert scores == sorted(scores, reverse=True)
```

---

### US-2: View topic timeline

> As a user, I want to open a topic and view its timeline, so that I can understand how the event evolved.

| Case ID | Scenario | Layer | Priority |
|---------|----------|-------|----------|
| SCT-US2-1 | Timeline returns events sorted by event_time ASC | API | High |
| SCT-US2-2 | Each event includes title, event_time, and source reference | API | High |
| SCT-US2-3 | Non-existent slug returns 404 with TOPIC_NOT_FOUND error code | API | High |
| SCT-US2-4 | Topic with no timeline events returns empty list, not an error | API | Medium |
| SCT-US2-5 | UI renders timeline in chronological order with source attribution | UI | High |

---

### US-3: See key entities

> As a user, I want to see key entities connected to a topic, so that I can understand who and what is driving the discussion.

| Case ID | Scenario | Layer | Priority |
|---------|----------|-------|----------|
| SCT-US3-1 | Topic detail response includes entities list | API | High |
| SCT-US3-2 | Each entity has name and entity_type (person/org/location) | API | High |
| SCT-US3-3 | Topic with no extracted entities returns empty entities list | API | Medium |
| SCT-US3-4 | UI renders entity badges grouped by type | UI | Medium |

---

### US-4: Read concise summary with sources

> As a user, I want a concise summary with supporting sources, so that I can trust the overview and continue exploring.

| Case ID | Scenario | Layer | Priority |
|---------|----------|-------|----------|
| SCT-US4-1 | Topic detail includes summary field (non-empty) | API | High |
| SCT-US4-2 | Source list returned with title, publisher, publish_time, url, snippet | API | High |
| SCT-US4-3 | Snippet is ≤ 500 characters | API | Medium |
| SCT-US4-4 | UI shows source attribution with publisher name and link | UI | High |

---

### US-5: Filter by category and geography

> As a user, I want to filter topics by category and geography, so that I can focus on what matters to me.

| Case ID | Scenario | Layer | Priority |
|---------|----------|-------|----------|
| SCT-US5-1 | `?region=domestic` returns only domestic topics | API | High |
| SCT-US5-2 | `?region=international` returns only international topics | API | High |
| SCT-US5-3 | `?category=economy` returns only economy category topics | API | High |
| SCT-US5-4 | Combined `?region=domestic&category=politics` filters correctly | API | High |
| SCT-US5-5 | Invalid region value returns 422 validation error | API | High |
| SCT-US5-6 | No matching results returns empty items list, not 404 | API | Medium |
| SCT-US5-7 | UI category filter chips update the list without page reload | UI | Medium |

---

### US-6: Search by keyword

> As a user, I want to search for a topic keyword, so that I can quickly find related threads and history.

| Case ID | Scenario | Layer | Priority |
|---------|----------|-------|----------|
| SCT-US6-1 | `GET /api/v1/search?q=tariff` returns relevant topics | API | High |
| SCT-US6-2 | Search respects category and region filters alongside q | API | High |
| SCT-US6-3 | Empty query string `q=` returns 400 or is treated as browse-all | API | Medium |
| SCT-US6-4 | Query longer than 200 chars returns 422 validation error | API | High |
| SCT-US6-5 | No matching results returns empty items list | API | Medium |
| SCT-US6-6 | Search input in UI debounces and triggers query on 300ms idle | UI | Low |

---

### US-7: Bookmark topics

> As a user, I want to bookmark important topics, so that I can revisit them later.

| Case ID | Scenario | Layer | Priority |
|---------|----------|-------|----------|
| SCT-US7-1 | `POST /api/v1/saved` with valid topic_id returns 201 | API | High |
| SCT-US7-2 | `GET /api/v1/saved` returns previously saved topics | API | High |
| SCT-US7-3 | `DELETE /api/v1/saved/{topic_id}` removes saved entry, returns 204 | API | High |
| SCT-US7-4 | Saving an already-saved topic is idempotent (no duplicate) | API | Medium |
| SCT-US7-5 | Saving non-existent topic_id returns 404 | API | Medium |
| SCT-US7-6 | UI bookmark icon toggles state immediately (optimistic update) | UI | Medium |

---

### US-8: Maintainable ingestion pipeline

> As a product team, we want a maintainable ingestion-to-insight pipeline, so that the system can scale beyond MVP.

| Case ID | Scenario | Layer | Priority |
|---------|----------|-------|----------|
| SCT-US8-1 | Worker processes a valid RSS feed and persists source documents | Integration | High |
| SCT-US8-2 | Duplicate content (same hash) is not inserted twice | Integration | High |
| SCT-US8-3 | Failed source fetch is logged and does not crash the worker | Integration | High |
| SCT-US8-4 | `GET /api/v1/health` returns 200 with status: ok | API | High |
| SCT-US8-5 | Worker completion is observable via structured log output | Integration | Medium |

---

## Priority Rules

| Priority | When to assign |
|----------|---------------|
| **High** | Happy path + any failure mode that blocks the User Story goal |
| **Medium** | Alternative paths, boundary values, graceful degradation |
| **Low** | UX polish, debounce, loading states, cosmetic behavior |

## Abnormal Case Design Rules

For each changed US, abnormal cases should cover three different failure classes when possible:

- Validation failure: bad query/body/path parameter -> expected 4xx.
- Data edge case: empty dataset or missing optional related data -> graceful response.
- Runtime degradation: upstream/source/service partial failure -> controlled error or fallback.

## Coverage Completeness Check

Before marking a User Story as tested, verify:
- [ ] Happy path works end-to-end
- [ ] At least 3 abnormal SCT cases implemented for this US
- [ ] Empty/no-data state handled
- [ ] Invalid input rejected with correct status code
- [ ] Required response fields all present and typed correctly
- [ ] UI reflects API state (loading, success, error)
