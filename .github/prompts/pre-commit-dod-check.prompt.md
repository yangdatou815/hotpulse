---
mode: ask
description: Run mandatory DoD gates before creating a commit.
---

Run a pre-commit DoD verification for the current staged/working changes.

Mandatory gates:
1. Coverage gate: changed modules must satisfy >= 90% unit test coverage.
2. SCT gate: for each changed User Story (from PRD section 6), there must be >= 1 normal and >= 3 abnormal SCT cases.
3. Smoke gate: critical smoke tests must pass.

Input context:
- Changed files:
${input:changed_files}
- Changed user stories (if any):
${input:changed_user_stories}

Required output:

DoD Result: PASS or FAIL

Coverage:
- command/result summary
- threshold check

SCT Mapping:
- US id -> normal count, abnormal count, pass/fail

Smoke:
- command/result summary
- pass/fail

Blocking Items:
- list items if FAIL

If DoD Result is FAIL, do not produce commit text.
