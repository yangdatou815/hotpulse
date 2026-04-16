---
mode: ask
description: Scaffold a new domain feature across backend module + frontend feature folder.
---

Scaffold a new feature: **${input:feature_name}**

Backend (FastAPI):
1. Create `backend/app/modules/${input:feature_name}/` with:
   - `__init__.py`
   - `router.py` — APIRouter with prefix `/${input:feature_name}`
   - `schemas.py` — Request and Response Pydantic v2 models
   - `models.py` — SQLAlchemy 2.x mapped model with `TimestampMixin`
   - `service.py` — async service functions using `AsyncSession`
2. Register the router in `backend/app/main.py`
3. Create `backend/migrations/versions/` Alembic migration for the new table

Frontend (React + TypeScript):
1. Create `frontend/src/features/${input:feature_name}/` with:
   - `index.ts` — barrel export
   - `api.ts` — TanStack Query hooks (`useQuery` / `useMutation`)
   - `types.ts` — TypeScript interfaces matching backend schemas
   - `${input:feature_name}List.tsx` — list component
   - `${input:feature_name}Card.tsx` — card component
2. Create placeholder page in `frontend/src/pages/` and register route in `frontend/src/app/router.tsx`

Follow all conventions in `.github/copilot-instructions.md`.
