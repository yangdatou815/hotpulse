---
applyTo: "backend/app/modules/**/router.py,backend/app/modules/**/schemas.py"
---

# API Design Guidelines — HotPulse

## Route Structure
- Base prefix: `/api/v1`
- Group routes by domain: `/topics`, `/search`, `/saved`
- Use nouns for resources, not verbs
- Nested resources only one level deep: `/topics/{slug}/timeline`

## HTTP Methods and Semantics
| Method | Usage |
|--------|-------|
| GET    | Read, idempotent, safe |
| POST   | Create new resource |
| PUT    | Full replacement |
| PATCH  | Partial update |
| DELETE | Remove resource |

## Request/Response Schema Rules
- Always use Pydantic v2 models for both request and response
- Response schemas must be explicit — never return ORM objects directly
- Use `response_model=` on every endpoint decorator
- All timestamps must be ISO 8601 in UTC: `2026-04-14T09:30:00Z`
- Paginated responses must wrap list in `{ "items": [...], "total": N, "page": N, "size": N }`

## Pagination
```python
class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
```
Default: `page=1`, `size=20`, `max_size=100`

## Error Format
All errors return a consistent envelope:
```json
{
  "error": {
    "code": "TOPIC_NOT_FOUND",
    "message": "Topic with slug 'xyz' not found",
    "details": {}
  }
}
```
- 400: Validation error (Pydantic handles automatically)
- 404: Resource not found
- 422: Unprocessable entity
- 500: Internal server error (never expose stack traces)

## Input Validation Rules
- All string inputs: strip whitespace, enforce max length
- `q` search param: max 200 chars
- Slugs: must match `^[a-z0-9-]+$`
- Enums for region, category, sort, freshness — never free-form strings for filters

## Query Parameters Convention
```
GET /api/v1/topics?region=international&category=economy&sort=heat&q=tariff&page=1&size=20
```

## FastAPI Router Pattern
```python
# router.py
router = APIRouter(prefix="/topics", tags=["topics"])

@router.get("", response_model=PaginatedResponse[TopicSummary])
async def list_topics(
    filters: TopicFilters = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[TopicSummary]:
    return await topic_service.list_topics(db, filters)
```

## Service Layer Contract
- Routers only: parse input, call service, return response
- Services handle: business logic, DB queries, error raising
- Services must raise `HTTPException` or domain exceptions — not return error codes
- No DB session creation inside services — pass db as parameter

## API Versioning
- Current: `/api/v1`
- Breaking changes always create new version path
- Old versions deprecate with `Deprecated: true` header before removal

## Documentation
- Every endpoint must have a docstring summary (shown in OpenAPI)
- Use `summary=` and `description=` in route decorators for complex endpoints
