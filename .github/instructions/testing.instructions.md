---
applyTo: "backend/tests/**,frontend/src/**/*.{test,spec}.{ts,tsx}"
---

# Testing Guidelines — HotPulse

## DoD Quality Gates (Mandatory)

All changes must satisfy these gates before commit/merge:

- Unit test coverage must be >= 90% for changed backend/frontend modules.
- For each changed User Story (US), SCT must include at least:
    - 1 normal (happy-path) case
    - 3 abnormal cases (validation/error/empty-state/boundary)
- Smoke test suite must pass for critical user flows.

If any gate fails, the change is not DoD-complete.

## Testing Strategy

```
                    E2E (Playwright)
                   ┌─────────────┐
                   │  UI flows   │  ← few, slow, critical paths only
                   └─────────────┘
            Integration (pytest + httpx)
           ┌──────────────────────────┐
           │  API contract tests      │  ← one per endpoint
           └──────────────────────────┘
    Unit (pytest / vitest)
   ┌──────────────────────────────────────┐
   │  Services, utils, transformers       │  ← most tests, fast, isolated
   └──────────────────────────────────────┘
```

## Backend Tests (pytest)

### Structure
```
backend/tests/
├── conftest.py           # fixtures: db, app client, seed data
├── unit/
│   ├── test_clustering.py
│   ├── test_summarizer.py
│   └── test_entity_extractor.py
└── integration/
    ├── test_topics_api.py
    ├── test_search_api.py
    └── test_saved_api.py
```

### conftest.py Pattern
```python
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:test@localhost/hotpulse_test"

@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def db(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture
async def client(db):
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
```

### Integration Test Pattern
```python
@pytest.mark.asyncio
async def test_list_topics_returns_paginated_response(client, seed_topics):
    response = await client.get("/api/v1/topics?region=international&page=1&size=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) <= 5

async def test_topic_detail_not_found(client):
    response = await client.get("/api/v1/topics/nonexistent-slug")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "TOPIC_NOT_FOUND"
```

### Unit Test Pattern
```python
def test_heat_score_returns_zero_for_no_sources():
    result = calculate_heat_score(source_count=0, recency_hours=48)
    assert result == 0

def test_slug_generation_is_url_safe():
    slug = generate_slug("US Tariff Policy: What Changed?")
    assert re.match(r'^[a-z0-9-]+$', slug)
```

## Frontend Tests (vitest + testing-library)

### Structure
```
frontend/src/
├── features/topics/__tests__/
│   ├── TopicCard.test.tsx
│   └── useTopics.test.ts
└── lib/__tests__/
    └── utils.test.ts
```

### Component Test Pattern
```tsx
import { render, screen } from "@testing-library/react"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { TopicCard } from "../TopicCard"
import { mockTopic } from "./fixtures"

const wrapper = ({ children }) => (
  <QueryClientProvider client={new QueryClient()}>
    {children}
  </QueryClientProvider>
)

test("shows heat score and title", () => {
  render(<TopicCard topic={mockTopic} />, { wrapper })
  expect(screen.getByText(mockTopic.title)).toBeInTheDocument()
  expect(screen.getByText("87")).toBeInTheDocument()
})
```

### Hook Test Pattern
```ts
import { renderHook, waitFor } from "@testing-library/react"
import { useTopics } from "../useTopics"

test("fetches topics with region filter", async () => {
  const { result } = renderHook(() => useTopics({ region: "international" }))
  await waitFor(() => expect(result.current.isSuccess).toBe(true))
  expect(result.current.data?.items.length).toBeGreaterThan(0)
})
```

## What to Test
| Must test | Optional |
|-----------|----------|
| Service layer business logic | Simple getters/setters |
| API endpoint contracts (happy + error paths) | Pure passthrough routes |
| Heat score and clustering algorithms | Static config values |
| Pagination edge cases (empty, last page) | Framework internals |
| Input validation rejection | Already-validated data |

## Smoke Test Set (Mandatory)

Define and keep a smoke suite for these flows:

- Smoke-1: topics list can be loaded (`GET /api/v1/topics` returns 200).
- Smoke-2: topic detail page can be opened (`GET /api/v1/topics/{slug}` returns 200 for seeded slug).
- Smoke-3: search endpoint returns response envelope (`GET /api/v1/search?q=<keyword>` returns 200).
- Smoke-4: save flow works (`POST /api/v1/saved` then `GET /api/v1/saved` includes the topic).
- Smoke-5: health endpoint is healthy (`GET /api/v1/health` returns 200 and status ok).

Smoke tests are fast checks and run in CI for every PR.

## Running Tests
```bash
# Backend
cd backend
pytest tests/ -v --tb=short --cov=app --cov-report=term-missing

# Frontend
cd frontend
npm test -- --run

# E2E (when configured)
npx playwright test
```

## DoD Verification Commands

Run these before commit:

```bash
# Backend coverage gate (>= 90%)
cd backend
pytest tests/ -q --cov=app --cov-report=term-missing --cov-fail-under=90

# Frontend tests
cd ../frontend
npm test -- --run

# Optional smoke marker if configured in pytest
cd ../backend
pytest tests/ -m smoke -q
```
