---
mode: ask
description: Write a well-scoped Conventional Commit message for staged changes.
---

Generate a Conventional Commit message for the following staged changes.

Before generating the commit message, run a DoD pre-check and include the check result in output.

Rules:
- Format: `<type>(<scope>): <summary>`
- Type must be one of: feat, fix, refactor, perf, test, docs, chore, style, ci, revert
- Scope must match the affected area: topics, search, ingestion, saved, db, api, ui, infra, deps, config
- Summary: imperative mood, max 72 chars, no period at end
- If changes span multiple scopes, pick the most significant one
- If breaking change, append `!` after type/scope
- Add a body paragraph if the change is non-obvious
- Add `BREAKING CHANGE:` footer only if the API contract or data model changed incompatibly

DoD pre-check must report:
- Coverage status (>= 90% pass/fail)
- SCT status for changed User Stories (>= 1 normal + >= 3 abnormal each)
- Smoke test status (pass/fail)

If any DoD item fails, do not output a final commit message. Output:
`DoD check failed` and list blocking items.

Staged diff or description of changes:
${input:changes}
