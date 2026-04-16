---
applyTo: "PRD.md,.github/instructions/**,.github/prompts/**,backend/**,frontend/**,.github/workflows/**"
---

# PRD Change Adaptation Workflow

## Purpose
When `PRD.md` changes, related skills, prompts, API contracts, tests, and delivery workflow must be adapted together.
This file defines the required dependency mapping and adaptation sequence.

## Trigger
Run this workflow when any of the following in `PRD.md` changes:
- MVP scope (in-scope / out-of-scope)
- User stories
- Functional requirements
- API specification
- Data model overview
- Non-functional requirements (performance/reliability/security)
- Implementation phases

## Section-to-Artifact Mapping

| PRD section changed | Must review/update |
|---|---|
| 5 MVP Scope | `.github/instructions/api-design.instructions.md`, `.github/instructions/testing.instructions.md`, `.github/prompts/new-feature.prompt.md` |
| 6 User Stories | `.github/instructions/sct-from-user-stories.instructions.md`, `.github/prompts/generate-sct-from-user-story.prompt.md` |
| 9 Core Features | `frontend/src/features/**` structure plan, `backend/app/modules/**` boundaries |
| 10 Functional Requirements | API schemas/routes, integration tests, error envelopes |
| 11 Non-Functional Requirements | CI checks, test thresholds, performance assertions |
| 12 Content Processing Pipeline | `.github/instructions/ingestion.instructions.md`, worker test strategy |
| 13 Architecture & Patterns | repository structure conventions and module boundaries |
| 14 Technology Stack | dependency policy, tooling prompts, CI setup |
| 16 API Specification | `.github/instructions/api-design.instructions.md`, API test cases |
| 17 Data Model Overview | `.github/instructions/database.instructions.md`, migration strategy |
| 19 Implementation Phases | prompts for scaffolding and sequencing |
| 20 Risks & Mitigations | review checklist severity and negative test cases |

## Mandatory Adaptation Steps

1. Diff PRD changes and classify impact by section.
2. Build impacted artifact list using the mapping table above.
3. Update instruction files first (policy and guardrails).
4. Update prompt files second (execution templates).
5. Update code/test/CI implications third (if required by changed requirements).
6. Add or update SCT cases for changed user stories.
7. Run a consistency pass:
   - Terms used in PRD match terms used in instructions/prompts.
   - Endpoint names and fields are consistent across PRD, API guidance, and tests.
   - Priority/performance targets reflected in testing and CI guidance.

## Definition of Done

A PRD change is not complete until all are true:
- Impacted instruction files updated.
- Impacted prompt files updated.
- SCT mapping for changed user stories updated.
- API/data model guidance synchronized with PRD text.
- CI/testing guidance aligned with latest non-functional requirements.
- Unit test coverage gate set to >= 90% and enforced in CI guidance.
- For each changed User Story: SCT includes >= 1 normal + >= 3 abnormal cases.
- Smoke test suite exists and is included in CI checks.
- Commit workflow includes pre-commit DoD verification.

## Output Format for Adaptation Work

Always produce:
1. `Impact Summary` (changed PRD sections + impacted files)
2. `Applied Updates` (exact files edited)
3. `Residual Gaps` (anything intentionally deferred)
4. `Validation` (what was checked for consistency)
