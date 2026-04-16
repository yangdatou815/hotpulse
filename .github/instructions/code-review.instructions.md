---
applyTo: "backend/**/*.py,frontend/src/**/*.{ts,tsx}"
---

# Code Review Guidelines — HotPulse

## Review Priority Order
1. Security (blocking)
2. Correctness (blocking)
3. Performance (non-blocking unless severe)
4. Maintainability (non-blocking)
5. Style (non-blocking)

---

## Security Checklist

### Backend (Python/FastAPI)
- [ ] No raw SQL strings — always use SQLAlchemy ORM or parameterized queries
- [ ] No secrets or credentials in source code — must use `os.getenv()` or config from env
- [ ] All user inputs validated via Pydantic before use
- [ ] HTTP errors never expose stack traces or internal details
- [ ] No `eval()`, `exec()`, or `subprocess` with unsanitized input
- [ ] `CORS` origins are explicit — never `*` in production config
- [ ] Rate limiting applied on public endpoints

### Frontend (TypeScript/React)
- [ ] No `dangerouslySetInnerHTML` with unsanitized content
- [ ] No secrets in client-side code or `VITE_` env vars that should be private
- [ ] External URLs validated before use in `<a href>` or `window.location`
- [ ] No user content rendered without escaping

---

## Correctness Checklist

### Backend
- [ ] Async functions are truly async — no blocking I/O in async handlers
- [ ] DB sessions properly closed — use `async with` or dependency injection
- [ ] `None` checks before accessing optional fields
- [ ] Pagination math correct: `offset = (page - 1) * size`
- [ ] No silent exception swallowing (`except: pass`)
- [ ] All code paths return a value or raise explicitly

### Frontend
- [ ] Query keys are stable and specific enough to avoid cache collisions
- [ ] Loading and error states handled — no silent failures in `useQuery`
- [ ] Form submissions are not duplicated on re-renders
- [ ] List items have stable `key` props (never use array index for mutable lists)

---

## Performance Checklist

### Backend
- [ ] No N+1 queries — use `selectinload()` or `joinedload()` for relations
- [ ] Heavy computations happen in workers, not in the request path
- [ ] Paginated queries use `LIMIT`/`OFFSET` or cursor pagination
- [ ] Indexes exist on commonly filtered columns: `region`, `category`, `heat_score`

### Frontend
- [ ] Large lists use virtualization (react-window) when > 100 items
- [ ] Images have explicit width/height to prevent layout shift
- [ ] Heavy components lazy-loaded with `React.lazy`
- [ ] No re-renders from object/array literals in JSX (`{}` and `[]` are new refs each render)

---

## Maintainability Checklist
- [ ] Module boundary respected — no cross-module direct imports of internal logic
- [ ] New domain logic in service layer, not in router/component
- [ ] No magic numbers — use named constants
- [ ] Function does one thing — split if doing multiple unrelated concerns
- [ ] Tests exist for new business logic paths

---

## Review Comment Format
Use severity prefix in comments:
- `[BLOCKER]` — Must fix before merge (security, correctness)
- `[MAJOR]` — Should fix before merge (performance, design)
- `[MINOR]` — Can fix in follow-up (style, naming)
- `[NIT]` — Optional polish

Example:
```
[BLOCKER] This query is susceptible to N+1: fetching sources inside a topics loop.
Use selectinload(Topic.sources) in the initial query.
```
