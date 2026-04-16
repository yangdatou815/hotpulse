# HotPulse — Copilot Project Instructions

## Project Overview
HotPulse is a topic intelligence web product. Users can see trending topics, understand their evolution via timelines, identify key entities, and read source-backed summaries.

## Tech Stack
- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.x, Alembic, PostgreSQL, Pydantic v2
- **Frontend**: React 18, Vite 5, TypeScript, Tailwind CSS, TanStack Query, React Router, Recharts
- **Infra**: Docker, docker-compose, PostgreSQL

## Repository Structure
```
hotpulse/
├── backend/          # FastAPI app, workers, tests
├── frontend/         # React SPA
├── infra/            # Docker and compose files
└── .github/          # CI/CD workflows, Copilot instructions, prompts, and skills
```

## AI Config Layout (IDE-agnostic)
- Shared instructions: `.github/instructions/*.instructions.md`
- Reusable prompts: `.github/prompts/*.prompt.md`
- Project baseline guidance: `.github/copilot-instructions.md`

## Key Conventions

### Backend
- All API routes live under `/api/v1/`
- Domain modules live in `backend/app/modules/{domain}/`
- Each module has: `router.py`, `schemas.py`, `models.py`, `service.py`
- Services are pure functions or classes — no FastAPI dependencies inside
- All DB access goes through SQLAlchemy async sessions
- Pydantic v2 schemas for all API I/O and validation
- Alembic for all schema migrations — never modify tables directly

### Frontend
- Feature-oriented structure under `src/features/{feature}/`
- Pages just compose features and layouts — no business logic in pages
- All API calls go through `src/lib/api.ts`
- TanStack Query for all async state — no raw useEffect for data fetching
- Tailwind utility classes only — no inline styles, no external component libraries

### General
- Never hardcode secrets — use environment variables
- Every public API endpoint must have input validation
- All summaries retain source attribution references
- Domain logic is tested at unit level; integration tests cover API contracts

## Naming Conventions
- Python: `snake_case` for files, functions, variables; `PascalCase` for classes
- TypeScript: `camelCase` for variables/functions; `PascalCase` for components/types
- DB tables: `snake_case` plural (e.g., `topic_events`)
- API slugs: `kebab-case`
