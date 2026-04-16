---
mode: ask
description: Adapt all impacted skills/prompts/tests after PRD.md changes.
---

You are adapting the repository after changes in `PRD.md`.

## Inputs
- PRD diff (or changed sections):
${input:prd_diff_or_sections}

## Required process
1. Identify changed PRD sections (5, 6, 9, 10, 11, 12, 13, 14, 16, 17, 19, 20).
2. Build an impact matrix using `.github/instructions/prd-change-adaptation.instructions.md`.
3. Update all impacted files in:
   - `.github/instructions/`
   - `.github/prompts/`
4. If API/data model requirements changed, also update related test guidance.
5. If user stories changed, regenerate SCT mapping and case templates.

## Hard constraints
- Keep existing style and naming conventions.
- Do not remove unrelated content.
- Preserve backward compatibility unless PRD explicitly introduces a breaking change.

## Required output
Return in this format:

### Impact Summary
- Changed PRD sections:
- Impacted files:

### Edits Applied
- file path + one-line reason per file

### Consistency Checks
- Terminology sync:
- API field/endpoint sync:
- NFR sync (performance/reliability/security):

### Follow-ups
- Any remaining manual tasks or open ambiguities
