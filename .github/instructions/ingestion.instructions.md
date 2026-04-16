---
applyTo: "backend/workers/**,backend/app/modules/ingestion/**"
---

# Ingestion Pipeline Guidelines — HotPulse

## Pipeline Stages
```
RSS/HTTP Sources
      │
      ▼
  [Fetcher]          fetch_source(url) → RawDocument
      │
      ▼
  [Normalizer]       normalize(raw) → NormalizedDocument
      │                ├── strip HTML
      │                ├── extract snippet (≤500 chars)
      │                ├── compute content hash (SHA-256)
      │                └── classify region + category
      │
      ▼
  [Deduplicator]     skip if content_hash already in DB
      │
      ▼
  [Clusterer]        assign to existing Topic or create new one
      │
      ▼
  [Entity Extractor] extract Person / Org / Location via NLP or regex
      │
      ▼
  [Summarizer]       generate/update topic summary from top sources
      │
      ▼
  [DB Writer]        upsert Topic, insert SourceDocument, Events, Entities
```

## Worker Schedule (APScheduler or cron)
| Job | Interval | Description |
|-----|----------|-------------|
| `ingest_all_sources` | every 15 min | fetch and process all active sources |
| `recalculate_heat_scores` | every 5 min | update heat scores based on recency + volume |
| `prune_stale_topics` | daily | mark topics as `fading` after inactivity threshold |

## Resilience Rules
- Each source failure is isolated — log and continue, never crash the worker
- Use exponential backoff for transient HTTP errors (3 retries max)
- Record `last_fetched_at` and `last_error` per source
- Content hash deduplication prevents re-processing identical articles

## Data Storage Rules
- Store: title, publisher, publish_time, url, snippet (≤500 chars), hash
- Never store full copyrighted article body
- Source attribution (publisher + url) must be preserved on all derived content

## Heat Score Formula (MVP)
```python
def calculate_heat_score(source_count: int, recency_hours: float) -> int:
    recency_factor = max(0.0, 1.0 - recency_hours / 72.0)
    volume_factor = min(1.0, source_count / 50.0)
    raw = (0.6 * recency_factor + 0.4 * volume_factor) * 100
    return round(raw)
```

## Clustering Strategy (MVP — Heuristic First)
1. Normalize title tokens (lowercase, remove stopwords)
2. Check for shared Named Entities with existing open topics (last 72h)
3. If title token overlap > 40% with existing topic → assign to it
4. Otherwise → create new topic
5. Topic summarizer runs after assignment if source_count changes

## Environment Variables
```
INGESTION_INTERVAL_MINUTES=15
MAX_RETRIES=3
SNIPPET_MAX_CHARS=500
TOPIC_STALENESS_HOURS=72
```
