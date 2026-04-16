---
mode: ask
description: Scaffold a new API endpoint (router + schema + service) for a given domain module.
---

Create a new FastAPI endpoint for the **${input:module}** module with the following spec:
- HTTP method: ${input:method}
- Path: ${input:path}
- Description: ${input:description}

Follow the project's API design guidelines:
1. Create or update the router in `backend/app/modules/${input:module}/router.py`
2. Add request/response Pydantic v2 schemas in `backend/app/modules/${input:module}/schemas.py`
3. Add business logic in `backend/app/modules/${input:module}/service.py`
4. Use `Depends(get_db)` for the DB session — never create sessions inside services
5. Return proper HTTP status codes and the standard error envelope on failure
6. Add docstring to the endpoint for OpenAPI documentation
7. Write a basic integration test in `backend/tests/integration/test_${input:module}_api.py`
