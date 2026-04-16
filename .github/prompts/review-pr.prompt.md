---
mode: ask
description: Review staged or changed code for security, correctness, and quality issues before committing.
---

Review the following code changes in this pull request / diff. Apply the HotPulse code review guidelines.

For each issue found, output in this format:
```
[SEVERITY] File: path/to/file.py (line N)
Issue: <description>
Fix: <concrete suggestion or code snippet>
```

Severity levels: `[BLOCKER]`, `[MAJOR]`, `[MINOR]`, `[NIT]`

Check for:
1. **Security**: SQL injection, XSS, exposed secrets, missing input validation, unsafe CORS
2. **Correctness**: Missing null checks, incorrect pagination math, swallowed exceptions, async/sync mismatches
3. **Performance**: N+1 queries, missing indexes accessed in the diff, blocking I/O in async handlers
4. **Maintainability**: Business logic in wrong layer (router/component instead of service), magic numbers, missing tests for new logic

At the end, provide a summary:
- Blocker count: N
- Major count: N
- Approved: yes / no (approved only if blocker count = 0)
