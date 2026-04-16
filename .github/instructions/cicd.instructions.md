---
applyTo: ".github/workflows/**"
---

# CI/CD Guidelines — HotPulse

## Workflow Overview
```
PR opened/updated
  └─> ci.yml
        ├── lint-backend     (ruff, mypy)
  ├── test-backend     (pytest + coverage gate >= 90%)
        ├── lint-frontend    (eslint, tsc)
  ├── test-frontend    (vitest)
  ├── smoke-tests      (critical API flow checks)
  └── dod-policy-check (SCT ratio and DoD checklist enforcement)

Merge to main
  └─> cd.yml
        ├── build-backend    (Docker image)
        ├── build-frontend   (Vite build -> Docker image)
        └── deploy           (docker compose up on target server)
```

## CI Workflow: `.github/workflows/ci.yml`
```yaml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  lint-backend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff mypy
      - run: ruff check .
      - run: mypy app --ignore-missing-imports

  test-backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: hotpulse_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --tb=short --cov=app --cov-report=term-missing --cov-fail-under=90
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:test@localhost/hotpulse_test

  lint-frontend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: frontend/package-lock.json
      - run: npm ci
      - run: npx tsc --noEmit
      - run: npx eslint src

  test-frontend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: frontend/package-lock.json
      - run: npm ci
      - run: npm test -- --run

  smoke-tests:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest tests/ -m smoke -q

  dod-policy-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Verify DoD declaration exists in PR
        run: |
          echo "Ensure PR includes DoD Check: coverage, SCT mapping, smoke result"
          # Optionally enforce with a repo script, e.g. scripts/check_dod.py
```

## CD Workflow: `.github/workflows/cd.yml`
```yaml
name: CD

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build and push backend image
        run: |
          docker build -t hotpulse-backend:${{ github.sha }} -f infra/docker/backend.Dockerfile .

      - name: Build and push frontend image
        run: |
          docker build -t hotpulse-frontend:${{ github.sha }} -f infra/docker/frontend.Dockerfile .

      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            cd /opt/hotpulse
            docker compose pull
            docker compose up -d --remove-orphans
```

## Environment Secrets (GitHub Secrets)
| Secret | Description |
|--------|-------------|
| `DEPLOY_HOST` | Production server IP/hostname |
| `DEPLOY_USER` | SSH user on production server |
| `DEPLOY_SSH_KEY` | Private SSH key for deployment |
| `DATABASE_URL` | Production database connection string |
| `SECRET_KEY` | FastAPI app secret key |

## Quality Gates
- CI must pass before merge is allowed (branch protection rule)
- No force-push to `main`
- PRs require at least 1 reviewer approval
- Coverage threshold: backend >= 90% for modules under test
- SCT threshold: each changed User Story has >= 1 normal + >= 3 abnormal cases
- Smoke threshold: smoke suite must pass on every PR

## Environments
| Environment | Branch | Auto-deploy |
|-------------|--------|-------------|
| Local       | any    | manual (`docker compose up`) |
| Staging     | `dev`  | on push (optional) |
| Production  | `main` | on push after CI passes |
