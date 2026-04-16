# Product Requirements Document (PRD)

## HotPulse MVP

## 1. Executive Summary

HotPulse is a full-stack web product for understanding the evolving structure behind international and domestic hot topics. It is not just a news feed and not just a trend list. The core value is to help users see the topic itself, the timeline, the key actors, and the representative sources behind the discussion.

The product should feel concise, calm, and premium. The interface must avoid information noise while still supporting high-density insight reading. Users should be able to answer five questions quickly:

- What is trending now?
- Why is it trending?
- How did the topic evolve over time?
- Who are the main actors in the topic?
- Which sources best explain the topic?

The MVP goal is to deliver a web application with a clean frontend and a practical backend that aggregates a curated set of sources, clusters related content into topics, generates a readable timeline-oriented topic thread, and provides a compact exploration experience. Cross-region comparison, advanced graph analysis, and heavy AI features are intentionally deferred.

## 2. Mission

### Mission Statement

Help users understand the context and evolution behind fast-moving热点 instead of only consuming fragmented headlines.

### Core Principles

- Context over clickbait.
- Clarity over dashboard overload.
- Signal over noise.
- Elegant reading experience over raw data dumping.
- Production-oriented architecture even within MVP scope.

## 3. Target Users

### Primary Personas

1. Information-sensitive professionals
- Need a fast grasp of what happened, why it matters, and how the narrative changed.
- Care about international affairs, macro trends, policy, technology, finance, and public discourse.

2. Content researchers and analysts
- Need to track topic evolution, related actors, and cross-source patterns.
- Prefer structured views over endless feed scrolling.

3. Curious general readers
- Want to understand major events without reading dozens of articles.
- Need simple but trustworthy visual explanations.

### Technical Comfort Level

- Moderate web literacy assumed.
- Desktop-first for deep reading and analysis.
- Mobile should support quick scan and save-for-later behavior.

### User Needs and Pain Points

- Need a single place to understand a topic thread, not just isolated posts.
- Need time-ordered narrative and source diversity.
- Need topic summaries that remain grounded in source evidence.
- Need distinction between domestic discourse and international discourse.
- Pain point with existing platforms: too noisy, too shallow, too feed-centric, too sensational.

## 4. Product Positioning

### Product Definition

HotPulse is a topic intelligence and context exploration web product.

### Not This

- Not a generic news portal.
- Not a short-video or content recommendation app.
- Not a stock-market terminal.
- Not a social media clone.

### This

- A clean topic intelligence dashboard.
- A narrative timeline explorer.
- A cross-source signal aggregator.
- A structured lens for domestic and international hotspots.

### MVP Narrowing Decisions

- Focus on topic discovery and topic understanding, not analyst-grade comparison.
- Start with curated news and official sources, not broad social network ingestion.
- Use reliable heuristics and source-backed summaries before advanced AI automation.
- Optimize for desktop-first reading depth while keeping mobile scan usable.

## 5. MVP Scope

### In Scope

#### Core Functionality

- Topic feed showing current hot topics.
- Topic clustering from multiple content sources.
- Topic detail page with:
  - summary
  - key timeline
  - core entities
  - representative source list
- Domestic and international tabs or filters.
- Search by keyword.
- Category filters such as politics, economy, technology, society, business, culture.
- Topic freshness indicator and heat score.
- Save/bookmark topic locally for later reading.
- Tag-based featured topic collections (e.g., US-Iran Conflict) with curated pills.
- Chinese/English language toggle with full UI internationalization.

#### Insight Functionality

- Event timeline generation.
- Entity extraction for people, organizations, locations.
- Multi-source summary with source references.

#### Technical

- Full-stack web app with separate frontend and backend.
- REST API for topic data and detail views.
- Scheduled ingestion and topic-processing pipeline.
- PostgreSQL for persistence.
- Search-ready schema design with PostgreSQL full-text search.
- Basic observability and logs.

#### Deployment

- Local development setup.
- Docker-based dev environment.
- Single-server production-ready deployment structure for frontend and API service.

### Out of Scope

#### Core Functionality

- User account system in MVP.
- Personalized recommendations.
- Comments or community features.
- Push notifications.
- Native mobile apps.
- Advanced multi-language translation workflow.
- Region-to-region topic comparison page.

#### Insight Functionality

- Full-scale knowledge graph editing.
- Topic relationship graph.
- Deep sentiment explainability.
- Analyst workspace collaboration.
- Automatic report export to PDF/PowerPoint.
- Automated topic-vs-topic compare view.

#### Technical

- Multi-tenant SaaS model.
- Complex billing or subscription system.
- Real-time websocket updates for every signal.
- Redis queueing and distributed worker scaling.

## 6. User Stories

1. As a user, I want to see the top hot topics now, so that I can identify the most important developments immediately.
2. As a user, I want to open a topic and view its timeline, so that I can understand how the event evolved.
3. As a user, I want to see key entities connected to a topic, so that I can understand who and what is driving the discussion.
4. As a user, I want a concise summary with supporting sources, so that I can trust the overview and continue exploring.
5. As a user, I want to filter topics by category and geography, so that I can focus on what matters to me.
6. As a user, I want to search for a topic keyword, so that I can quickly find related threads and history.
7. As a user, I want to bookmark important topics, so that I can revisit them later.
8. As a product team, we want a maintainable ingestion-to-insight pipeline, so that the system can scale beyond MVP.

## 7. UX Vision

### Design Direction

The product should feel editorial, restrained, and intelligent.

### Visual Style Keywords

- Minimal but premium.
- Light background with layered depth.
- Strong typography hierarchy.
- Generous whitespace.
- Quiet color system with one restrained accent.
- Dense information presented with calm rhythm.

### Interaction Principles

- The homepage should support scan-first behavior.
- The detail page should support read-deep behavior.
- Visual hierarchy must distinguish summary, evidence, and metadata.
- Motion should be subtle and purposeful.
- Charts and timelines should feel analytical, not flashy.

### Suggested Visual System

- Background: warm light gray (#f7f5f0) with subtle warmth, not pure white.
- Accent: muted teal (#2a6b5e) for primary actions and interactive states.
- Typography: Georgia serif for headlines and brand, system sans-serif (-apple-system, SF Pro, PingFang SC) for UI.
- Cards: soft border (#e2ddd5), low-contrast shadow, generous padding (22px+), 12px radius.
- Badges: color-coded pills for heat, freshness, region, category.
- Navigation: sticky top bar with glassmorphism blur effect.
- Hero strip: gradient accent background for editorial impact.
- Language toggle: compact button in top-right nav, switches all UI text between English and Chinese.
- Featured tag pills: red gradient accent pills for curated hot-spot collections (e.g., conflict tracking).
- Responsiveness: mobile-first with graceful downscaling at 640px breakpoint.

## 8. Information Architecture

### Primary Navigation

- Home
- Explore
- Saved

### Core Pages

#### 1. Home (/)

Purpose:
- Show the most important domestic and international topics.
- Provide instant overview and entry into deeper exploration.

Sections:
- Hero summary strip: gradient accent block with "What matters today" / "今日要闻" message.
- Featured tag pills for hot-spot collections (e.g., 🔴 US-Iran Conflict).
- Search bar with live filtering.
- Region filter pills (All / 国内 / 国际).
- Category filter pills (politics, economy, technology, society, business, culture).
- Topic card grid with heat score, freshness badge, region, category, and save action.

#### 2. Topic Detail (/topics/:slug)

Purpose:
- Present the full thread behind a topic.

Sections:
- Back-to-home link.
- Title and one-paragraph summary.
- Meta badges: heat score, freshness, region, category, source count.
- Save topic button.
- Timeline view with chronological dots.
- Key entities as tagged pills with type icons.
- Source stream with publisher, date, and snippet.

#### 3. Explore (/explore)

Purpose:
- Browse by category, region, and keyword.

Sections:
- Search input.
- Region and category filter pills.
- Topic grid/list.

#### 4. Saved (/saved)

Purpose:
- Revisit bookmarked topics.
- Remove saved topics inline.

## 9. Core Features

### Feature 1: Hot Topic Feed

- Rank topics by heat score.
- Display title, summary, category, region, freshness, and source count.
- Show whether the topic is rising, stable, or fading.

### Feature 2: Topic Clustering

- Group related articles/posts/signals into a topic thread.
- Deduplicate near-identical content.
- Maintain topic metadata and confidence score.

### Feature 3: Timeline View

- Order key events chronologically.
- Surface important changes in narrative or event state.
- Mark source-backed milestones.

### Feature 4: Entity View

- Extract entities from source documents.
- Show top entities tied to the topic.

### Feature 5: Search & Filter

- Search by keyword.
- Filter by region, category, and time range.
- Sort by heat and freshness.

### Feature 6: Save Topics

- Save topics locally in MVP.
- Allow quick return to saved items.

## 10. Functional Requirements

### Topic Feed Requirements

- System must return a paginated list of hot topics.
- Each topic item must include id, title, slug, summary, heat_score, freshness, region, category, source_count, updated_at.
- User must be able to filter by domestic or international.

### Topic Detail Requirements

- System must return a topic summary grounded in source data.
- System must return a timeline with at least title, timestamp, and source reference.
- System must return key entities.
- System must expose source list with title, publisher, publish_time, url, and snippet.

### Search Requirements

- Search should return relevant topics by keyword.
- Search response should support category and region filters.

## 11. Non-Functional Requirements

- First screen usable on desktop within 2.5 seconds on standard broadband.
- API p95 under 500ms for cached topic list endpoints.
- API p95 under 900ms for topic detail under normal development load.
- System must degrade gracefully when some upstream sources fail.
- All summaries must retain source attribution references.
- Frontend must be responsive on desktop and mobile.
- Backend jobs must be observable via logs.

## 12. Data Sources and Content Strategy

### Initial Source Types

- Major news websites.
- Public RSS feeds.
- Public official announcements.

### Source Principles

- Prefer structured and reputable sources.
- Avoid copying full copyrighted articles into the product.
- Store metadata, snippets, extracted entities, and links.
- Preserve source attribution clearly.

### Content Processing Pipeline

- Ingest source metadata and snippets.
- Normalize and deduplicate.
- Classify by category and region.
- Cluster into topics using heuristic-first logic.
- Extract entities and events.
- Generate summaries and timeline candidates.
- Cache results for frontend consumption.

## 13. Core Architecture & Patterns

### High-Level Architecture

- Frontend SPA consumes backend REST APIs.
- Backend API serves aggregated topic views.
- Scheduled worker process handles ingestion, clustering, extraction, and summarization.
- PostgreSQL stores topics, source documents, entities, and timeline items.

### Proposed Directory Structure

```text
hotpulse/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── db/
│   │   ├── modules/
│   │   │   ├── topics/
│   │   │   ├── search/
│   │   │   └── ingestion/
│   │   └── services/
│   ├── workers/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── pages/
│   │   ├── features/
│   │   ├── components/
│   │   ├── lib/
│   │   └── styles/
│   ├── package.json
│   └── vite.config.ts
├── infra/
│   ├── docker/
│   └── compose/
└── PRD.md
```

### Key Patterns and Principles

- Domain-oriented backend modules.
- Feature-oriented frontend structure.
- API-first contracts.
- Background jobs separated from request path.
- Clear split between raw source data and derived topic intelligence.
- Source attribution preserved end to end.
- Heuristic-first implementation before heavier ML or LLM dependencies.

## 14. Technology Stack

### Backend

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Pydantic v2
- Alembic

### Frontend

- React 18+
- Vite 5+
- TypeScript
- Tailwind CSS or CSS variables based design system
- TanStack Query
- React Router
- Recharts for restrained timeline and score views

### Search / AI / NLP Support

- PostgreSQL full-text search for MVP
- Lightweight entity extraction pipeline
- Template-driven or rule-assisted summary generation for MVP

### Testing

- Backend: pytest, httpx, pytest-asyncio
- Frontend: vitest, testing-library
- E2E: Playwright

## 15. Security & Compliance Considerations

### In Scope

- Input validation.
- Safe API error handling.
- Rate limiting for public APIs if exposed externally.
- Secrets via environment variables.
- Source attribution and link-back.
- Avoid storing unauthorized full copyrighted content.

### Out of Scope for MVP

- User authentication and RBAC.
- Enterprise audit logging.
- Data residency customization.

## 16. API Specification

### Base

- Base path: /api/v1
- Content type: application/json

### Endpoints

#### Topics

- GET /api/v1/topics
  - List topics with filters: region, category, sort, q, page.
- GET /api/v1/topics/{topic_slug}
  - Return topic detail.
- GET /api/v1/topics/{topic_slug}/timeline
  - Return timeline items.
- GET /api/v1/topics/{topic_slug}/sources
  - Return representative sources.

#### Search

- GET /api/v1/search?q=...
  - Return matching topics.

#### Saved

- GET /api/v1/saved
- POST /api/v1/saved
- DELETE /api/v1/saved/{topic_id}

#### System

- GET /api/v1/health

### Example Topic Response

```json
{
  "id": "topic_20260414_001",
  "slug": "us-tariff-policy-shift",
  "title": "US Tariff Policy Shift Triggers Global Supply Chain Debate",
  "summary": "Recent policy changes triggered renewed discussion across trade, manufacturing, and inflation topics.",
  "region": "international",
  "category": "economy",
  "heat_score": 87,
  "freshness": "rising",
  "source_count": 42,
  "updated_at": "2026-04-14T09:30:00Z"
}
```

## 17. Data Model Overview

### Core Entities

- Topic
- SourceDocument
- TimelineEvent
- Entity
- TopicMetric
- SavedTopic

### Key Relationships

- One Topic has many SourceDocuments.
- One Topic has many TimelineEvents.
- One Topic has many Entities through topic_entity links.

## 18. Success Criteria

### MVP Success Definition

Users can understand why a topic matters and how it evolved within 60 seconds of opening the topic detail page.

### Functional Success

- Users can browse hot topics by region.
- Users can open any topic and view summary, timeline, and sources.
- Users can search and filter topics.
- Users can save topics locally.

### Quality Indicators

- No P1 defects in topic list, topic detail, or saved flow.
- Stable ingestion for selected MVP sources.
- Core API and UI tests pass in CI.

### UX Goals

- Homepage scan in under 15 seconds.
- Topic understanding in under 60 seconds.
- Mobile quick scan in under 30 seconds.

## 19. Implementation Phases

### Phase 1: Foundation

Goal:
- Establish repo structure and basic stack.

Deliverables:
- Frontend and backend scaffolds.
- PostgreSQL local environment.
- Base API and homepage shell.
- Source ingestion proof of concept.

### Phase 2: Topic Feed and Detail

Goal:
- Deliver the main value loop.

Deliverables:
- Topic list API.
- Topic detail API.
- Summary and timeline UI.
- Source list and filters.

### Phase 3: Search and Hardening

Goal:
- Improve findability and release readiness.

Deliverables:
- Search endpoint and UI.
- Tests for critical flows.
- Performance improvements.
- Better loading and error states.
- Design polish and content quality checks.

## 20. Risks & Mitigations

1. Risk: Topic clustering quality is noisy.
- Mitigation: Start with limited source set and deterministic heuristics before complex models.

2. Risk: Summaries become generic or hallucinated.
- Mitigation: Start with template-driven summaries, require source grounding, and add deterministic validation rules.

3. Risk: UI becomes too dense and overwhelming.
- Mitigation: Keep layered disclosure and editorial hierarchy.

4. Risk: Source coverage is uneven across domestic and international topics.
- Mitigation: Define minimum viable source portfolio for each region.

5. Risk: Copyright and content compliance issues.
- Mitigation: Store metadata, snippets, extracted facts, and attribution rather than full article bodies when not permitted.

## 21. Open Questions for Review

- Should MVP prioritize desktop-only depth first, or keep full mobile parity from day one?
- Should summaries be template-driven first, or allow limited AI assistance from the start?
- Which source families are explicitly approved for ingestion in the first release?
- Is saved topics feature local-only enough for MVP, or do we want login earlier?

## 22. Appendix

### Suggested Product Names

- HotPulse
- HeatThread
- SignalAtlas
- TopicWeave
- PulseMap

### Recommended MVP Direction

HotPulse is recommended because it is short, web-friendly, and aligned with the product idea of tracking topic heat and movement.
