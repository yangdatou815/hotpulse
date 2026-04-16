# HotPulse Release Notes

## v0.2.0 — Tags, i18n & Featured Topics (2026-04-15)

### Summary

Added tag-based topic filtering for curated collections (e.g., US-Iran Conflict), a complete Chinese/English language toggle, and rich seed data for conflict coverage.

---

### New: Tag-Based Topic Filtering

- Topics can now have one or more tags (comma-separated in DB, array in API).
- `GET /api/v1/topics?tag=us-iran-conflict` filters topics by tag.
- `GET /api/v1/search?q=...&tag=...` also supports tag filtering.
- Featured tag pills on Home and Explore pages (e.g., "🔴 US-Iran Conflict").
- Tag badges displayed on topic cards (e.g., `#us-iran-conflict`, `#middle-east`).

**Files modified:** `models.py`, `schemas.py`, `service.py`, `router.py`, `search/router.py`, `api.ts`, `HomePage.tsx`, `ExplorePage.tsx`, `TopicCard.tsx`, `styles.css`

### New: Chinese/English Language Toggle (i18n)

- Language toggle button in the top-right of the navigation bar.
- Switches between English ("中文" button) and Chinese ("EN" button).
- All UI text is internationalized: navigation, hero, filters, badges, detail sections, empty states, buttons.
- Language preference persisted in `localStorage`.
- Date formatting adapts to locale (en-US / zh-CN).
- ~50 translation keys covering all pages.

**Files added:** `src/lib/i18n.tsx`
**Files modified:** `main.tsx`, `Layout.tsx`, `HomePage.tsx`, `TopicDetailPage.tsx`, `ExplorePage.tsx`, `SavedPage.tsx`, `TopicCard.tsx`, `styles.css`

### New: US-Iran Conflict Seed Data

- 3 detailed topics with rich bilingual content.
- 16 timeline events across all three topics.
- 12 entities (people, organizations, locations).
- 11 source documents from diverse outlets (Reuters, AP, CNN, BBC, 新华社, etc.).
- Tagged with `us-iran-conflict` and `middle-east`.

**Files added:** `workers/seed_iran.py`, `workers/tag_iran.py`

---

## v0.1.0 — MVP Foundation (2026-04-15)

### Summary

Established the full-stack MVP scaffold with a working backend API, premium-design frontend, comprehensive test suite, Docker-ready infrastructure, and a live ingestion pipeline that fetches real news from RSS feeds.

---

### Backend (Python / FastAPI)

#### API Endpoints Implemented

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/topics` | GET | Paginated topic list with region/category/keyword filters |
| `/api/v1/topics/{slug}` | GET | Topic detail with summary, timeline, entities, sources |
| `/api/v1/topics/{slug}/timeline` | GET | Timeline events for a topic |
| `/api/v1/topics/{slug}/sources` | GET | Source documents for a topic |
| `/api/v1/search?q=` | GET | Search topics by keyword with filters |
| `/api/v1/saved` | GET | List saved/bookmarked topics |
| `/api/v1/saved` | POST | Save a topic |
| `/api/v1/saved/{topic_id}` | DELETE | Remove a saved topic |
| `/api/v1/ingestion/run` | POST | Trigger ingestion pipeline manually |

#### Data Model

- **Topic**: id, slug, title, summary, region, category, heat_score, freshness, source_count, updated_at
- **TimelineEvent**: topic_id, title, timestamp, source
- **Entity**: name, entity_type (person/org/location)
- **TopicEntity**: many-to-many link with mention_count
- **SourceDocument**: topic_id, title, publisher, publish_time, url, snippet
- **SavedTopic**: topic_id, saved_at

#### Dependencies

- FastAPI 0.115.2, SQLAlchemy 2.0.35, Pydantic v2, Alembic 1.13.3, asyncpg
- Database: SQLite (dev) / PostgreSQL 16 (production)

#### Files

- `app/main.py` — FastAPI app with startup seeding
- `app/config.py` — Settings (app_name, api_prefix, database_url)
- `app/db/` — Base, session, seed data
- `app/modules/topics/` — models, router, schemas, service
- `app/modules/search/` — search router (delegates to topic service)
- `app/modules/saved/` — saved topics CRUD router
- `app/modules/ingestion/fetcher.py` — RSS feed fetcher with curated source list
- `app/modules/ingestion/clustering.py` — Heuristic topic clustering (Jaccard similarity)
- `app/modules/ingestion/entities.py` — Regex entity extraction (person/org/location)
- `app/modules/ingestion/pipeline.py` — Pipeline orchestrator: fetch → cluster → extract → persist
- `app/modules/ingestion/router.py` — Manual ingestion trigger API
- `workers/ingest.py` — Standalone worker (one-shot or loop mode)

---

### Frontend (React 18 / TypeScript / Vite)

#### Pages

| Page | Route | Description |
|------|-------|-------------|
| Home | `/` | Hero strip, search bar, region/category filter pills, topic card grid |
| Topic Detail | `/topics/:slug` | Full topic view with timeline, entities, sources, save button |
| Explore | `/explore` | Browse with search + filters |
| Saved | `/saved` | Bookmarked topics with remove action |

#### Design System

- Premium editorial aesthetic: warm gray background (#f7f5f0), muted teal accent (#2a6b5e)
- Georgia serif for headlines, system sans-serif for UI
- Sticky glassmorphism navigation bar
- Color-coded badges: heat (orange), rising (green), stable (gray), fading (red), region (teal), category (purple)
- Timeline with chronological dots and source references
- Entity tags with type icons (👤 person, 🏛 org, 📍 location)
- Mobile-responsive at 640px breakpoint

#### Dependencies

- React 18, React Router DOM 6, Vite 5, TypeScript 5
- @vitejs/plugin-react for HMR

#### Files

- `src/app/App.tsx` — Router setup
- `src/lib/api.ts` — Type-safe API client
- `src/components/layout/Layout.tsx` — Global layout + nav
- `src/components/ui/TopicCard.tsx` — Topic card component
- `src/pages/HomePage.tsx`
- `src/pages/TopicDetailPage.tsx`
- `src/pages/ExplorePage.tsx`
- `src/pages/SavedPage.tsx`
- `src/styles.css` — Full design system

---

### Test Suite

**34 backend tests — all passing** (pytest + httpx + aiosqlite in-memory)

| Module | Tests | PRD Coverage |
|--------|-------|-------------|
| `test_health.py` | 1 | System health endpoint |
| `test_topics.py` | 19 | UC1–UC5: topic list, detail, timeline, entities, sources, filters, pagination |
| `test_search.py` | 8 | UC6: keyword search, case-insensitive, summary match, filters, pagination |
| `test_saved.py` | 6 | UC7: save, list, delete, idempotent, not-found |

#### Test Files

- `tests/conftest.py` — In-memory SQLite fixtures, seed data
- `tests/test_health.py`
- `tests/test_topics.py`
- `tests/test_search.py`
- `tests/test_saved.py`

---

### Infrastructure

- `infra/docker/backend.Dockerfile` — Python 3.12 + uvicorn
- `infra/docker/frontend.Dockerfile` — Node 20 + vite dev
- `infra/compose/docker-compose.yml` — api + web + PostgreSQL 16
- `backend/alembic.ini` + `migrations/` — DB migration setup

---

### PRD Compliance

#### Fully Implemented ✅

- UC1: Hot topic feed ranked by heat_score
- UC2: Topic detail with timeline view
- UC3: Key entities connected to topics
- UC4: Summary with source attribution
- UC5: Filter by category and region (domestic/international)
- UC6: Search by keyword
- UC7: Save/bookmark topics
- Section 10: All functional requirements
- Section 16: All API endpoints
- Section 17: All data model entities

#### Partially Implemented ⚠️

- Section 14: Testing — backend complete; frontend/E2E tests deferred

#### Not Yet Implemented ❌

- TanStack Query (frontend uses native fetch + useEffect)
- Tailwind CSS (custom CSS design system used instead)
- Frontend tests (vitest / testing-library)
- E2E tests (Playwright)
- Advanced topic clustering (ML-based)
- Full NLP entity extraction

---

### Data Status

- **Seed data**: 1 example topic ("US Tariff Policy Shift")
- **Live ingestion**: 7 RSS sources configured (BBC, NYT, Ars Technica, Reuters, 人民网, 新华网, 36氪)
- Reachable sources produce ~20+ topics per run
- Pipeline: fetch → cluster → entity extraction → timeline → persist
- Trigger via: `POST /api/v1/ingestion/run` or `python -m workers.ingest`

---

### How to Run

#### Backend (SQLite dev mode)

```bash
cd backend
pip install -r requirements.txt aiosqlite
DATABASE_URL="sqlite+aiosqlite:///./hotpulse_dev.db" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npx vite --host 0.0.0.0 --port 5173
```

#### Docker Compose (full stack)

```bash
cd infra/compose
docker-compose up --build
```

#### Run Tests

```bash
cd backend
pip install pytest httpx pytest-asyncio aiosqlite eval_type_backport
python -m pytest tests/ -v
```

---

### Known Issues

- `on_event("startup")` is deprecated in FastAPI; should migrate to lifespan
- Python 3.9 compatibility requires `eval_type_backport` package
- Browser may cache old Vite build artifacts; use hard refresh (Ctrl+Shift+R) after code changes
