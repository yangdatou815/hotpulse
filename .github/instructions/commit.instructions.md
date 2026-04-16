---
applyTo: "**"
---

# Commit Conventions — HotPulse

## Format
Follow Conventional Commits: https://www.conventionalcommits.org

```
<type>(<scope>): <short summary>

[optional body]

[optional footer(s)]
```

## Types
| Type       | When to use |
|------------|-------------|
| `feat`     | New feature or user-visible functionality |
| `fix`      | Bug fix |
| `refactor` | Code restructure without behavior change |
| `perf`     | Performance improvement |
| `test`     | Adding or updating tests only |
| `docs`     | Documentation only |
| `chore`    | Build, config, dependencies, tooling |
| `style`    | Formatting, whitespace (no logic change) |
| `ci`       | CI/CD pipeline changes |
| `revert`   | Revert a previous commit |

## Scopes
| Scope        | Area |
|--------------|------|
| `topics`     | Topics module (backend or frontend) |
| `search`     | Search module |
| `ingestion`  | Ingestion pipeline and workers |
| `saved`      | Saved topics feature |
| `db`         | Database models, migrations |
| `api`        | General API / routing layer |
| `ui`         | Frontend UI components |
| `infra`      | Docker, compose, deployment config |
| `deps`       | Dependency updates |
| `config`     | Configuration files |

## Rules
- Summary line: max 72 characters, imperative mood ("add" not "added")
- No period at end of summary line
- Body: explain *what* and *why*, not *how*
- Breaking changes: add `!` after type or `BREAKING CHANGE:` in footer

## Pre-Commit DoD Gate (Mandatory)

Before creating any commit, verify DoD gates:

- Coverage gate: changed modules covered >= 90%.
- SCT gate: each changed User Story has >= 1 normal + >= 3 abnormal cases.
- Smoke gate: core smoke tests pass.

If any gate fails, do not commit.

Recommended local checklist:

```bash
# 1) Backend coverage
cd backend
pytest tests/ -q --cov=app --cov-report=term-missing --cov-fail-under=90

# 2) Frontend tests
cd ../frontend
npm test -- --run

# 3) Smoke tests
cd ../backend
pytest tests/ -m smoke -q
```

## Examples
```
feat(topics): add heat score sorting to topic feed API

Adds ?sort=heat query param support. Defaults to heat_score DESC.
Topics without a score are ranked last.

feat(ui)!: redesign topic card layout

BREAKING CHANGE: TopicCard props interface changed.
heat_score is now required.

fix(ingestion): handle empty RSS feed gracefully

fix(db): correct offset calculation in paginated queries

chore(deps): bump fastapi from 0.110 to 0.115

ci: add backend lint step to PR workflow
```

## Branch Naming
```
<type>/<scope>-<short-description>
```
Examples:
- `feat/topics-heat-score-sort`
- `fix/ingestion-empty-rss`
- `chore/deps-fastapi-bump`
- `ci/add-lint-step`

## PR Title
Same format as commit title. Must match the squash-merge commit.

PR description should include a `DoD Check` section with:
- Coverage result
- SCT mapping result (US -> cases)
- Smoke test result
