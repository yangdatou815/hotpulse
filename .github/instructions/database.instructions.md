---
applyTo: "backend/app/db/**,backend/migrations/**"
---

# Database & Migration Guidelines — HotPulse

## ORM Conventions (SQLAlchemy 2.x)

### Base Model
```python
# backend/app/db/base.py
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import func
import datetime

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )
```

### Naming Conventions
- Table names: `snake_case`, plural: `topics`, `source_documents`, `timeline_events`
- Primary key: `id` (UUID preferred, or `BIGINT` SERIAL for internal tables)
- Foreign keys: `{table_singular}_id`, e.g., `topic_id`
- Index names: `ix_{table}_{column}`, unique: `uq_{table}_{column}`
- Constraint names: `ck_{table}_{rule}`

## Core Schema

### topics
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | Primary key |
| slug | VARCHAR(255) | Unique, URL-safe |
| title | TEXT | Required |
| summary | TEXT | Source-grounded |
| region | VARCHAR(50) | `domestic` / `international` |
| category | VARCHAR(50) | `economy`, `politics`, etc. |
| heat_score | INT | 0-100 |
| freshness | VARCHAR(20) | `rising` / `stable` / `fading` |
| source_count | INT | Denormalized for perf |
| updated_at | TIMESTAMPTZ | |
| created_at | TIMESTAMPTZ | |

### source_documents
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | Primary key |
| topic_id | UUID | FK → topics |
| title | TEXT | |
| publisher | VARCHAR(255) | |
| publish_time | TIMESTAMPTZ | |
| url | TEXT | |
| snippet | TEXT | Max 500 chars |
| raw_content_hash | VARCHAR(64) | SHA-256 for dedup |

### timeline_events
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | Primary key |
| topic_id | UUID | FK → topics |
| title | TEXT | |
| description | TEXT | |
| event_time | TIMESTAMPTZ | |
| source_document_id | UUID | FK → source_documents |

### entities
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | Primary key |
| name | VARCHAR(255) | |
| entity_type | VARCHAR(50) | `person` / `org` / `location` |

### topic_entities (join table)
| Column | Type |
|--------|------|
| topic_id | UUID |
| entity_id | UUID |
| mention_count | INT |

### saved_topics (client-side MVP fallback, or server-side)
| Column | Type |
|--------|------|
| id | UUID |
| topic_id | UUID |
| saved_at | TIMESTAMPTZ |

## Migrations (Alembic)

### Setup
```bash
cd backend
alembic init migrations
# Set sqlalchemy.url in alembic.ini or use env variable
```

### Creating a Migration
```bash
# Auto-generate from model changes
alembic revision --autogenerate -m "add heat_score index to topics"

# Always review the generated file before applying!
alembic upgrade head
```

### Migration Rules
- Never write raw `ALTER TABLE` outside Alembic
- Every migration must be reversible — implement `downgrade()`
- Never delete columns immediately — use multi-step: nullable → backfill → drop
- Add indexes for: `region`, `category`, `heat_score`, `slug` (unique), `topic_id` on child tables
- Use `op.execute()` for data migrations, not model imports

### Recommended Indexes
```python
# In migration file
op.create_index("ix_topics_region", "topics", ["region"])
op.create_index("ix_topics_category", "topics", ["category"])
op.create_index("ix_topics_heat_score", "topics", ["heat_score"])
op.create_index("ix_source_documents_topic_id", "source_documents", ["topic_id"])
op.create_index("ix_timeline_events_topic_id", "timeline_events", ["topic_id"])

# Full-text search index
op.execute("CREATE INDEX ix_topics_fts ON topics USING gin(to_tsvector('english', title || ' ' || summary))")
```

## Session Management
```python
# backend/app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```
