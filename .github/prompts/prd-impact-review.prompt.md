---
mode: ask
description: Review PRD changes and report required downstream adaptations before editing files.
---

Analyze the latest `PRD.md` changes and produce a downstream adaptation plan.

Input PRD diff/summary:
${input:prd_change_summary}

Use `.github/instructions/prd-change-adaptation.instructions.md` as policy.

Output exactly these sections:

1. `Changed Sections`
- List PRD section numbers and brief change summary.

2. `Impact Matrix`
- For each changed section, list required file updates in `.github/instructions`, `.github/prompts`, tests, and CI.

3. `Risk of Drift`
- Identify where PRD and existing skills may diverge if not updated.

4. `Recommended Edit Order`
- Ordered list of files to update first to minimize inconsistency.

5. `Acceptance Checklist`
- A checklist to confirm adaptation completion.
