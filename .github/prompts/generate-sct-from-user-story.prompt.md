---
mode: ask
description: Design SCT test cases for a given User Story from the PRD.
---

Design SCT (System Component Test) cases for the following User Story from the HotPulse PRD.

**User Story ID:** US-${input:us_id}
**User Story:** ${input:user_story}

Related API endpoints and data from PRD:
- Base path: `/api/v1`
- Topic fields: `id, title, slug, summary, heat_score, freshness, region, category, source_count, updated_at`
- Paginated response: `{ items, total, page, size }`
- Error envelope: `{ error: { code, message, details } }`

Instructions:
1. Identify all test scenarios:
   - Happy path (the stated goal succeeds)
   - Empty/zero-result case
   - Invalid input / validation rejection
   - Any meaningful filter or parameter variants
   - Relevant UI state (loading, error, empty, populated)

2. For each scenario output a case spec block:
```
# SCT-US<id>-<N>
# User Story: <exact US text>
# Scenario:   <what this case covers>
# Priority:   High | Medium | Low
# Layer:      API | UI | E2E
#
# Precondition:
#   - <system state>
#
# Input:
#   - <HTTP method + path + params, or user action>
#
# Expected Output:
#   - <status code + response shape, or visible UI element>
```

3. Then output a **pytest async test function skeleton** for every API-layer case, using:
   - `async def test_<scenario>(client, ...):`
   - `await client.<method>("<path>")`
   - `assert response.status_code == <N>`
   - assertions on response JSON fields

4. Produce a **coverage summary table**:
   | Case ID | Scenario | Layer | Priority |
   |---------|----------|-------|----------|

5. List any **open questions** where PRD is ambiguous for this story.
