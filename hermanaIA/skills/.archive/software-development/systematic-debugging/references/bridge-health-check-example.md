# Bridge Health Check Example: memory_bridge.py

## Context
During a diagnostic session on 2026-05-14, the agent needed to assess the health and endpoints of a local bridge service (`memory_bridge.py`). The agent initially assumed common endpoints (`/status`, `/store`) which did not exist, leading to wasted time.

## Correct Approach
1. **Locate and read the bridge source code first** to understand its actual API.
2. Identify the actual endpoints from the code.
3. Test only the documented endpoints.

## memory_bridge.py Endpoints (Actual)
This bridge exposes only three GET endpoints:

- `GET /profile` → Returns bridge profile and version
- `GET /context` → Returns current memory context summary
- `GET /pending` → Returns queued memory entries

**No `/status` or `/store` endpoints exist.**

## Verification Commands
```bash
# Basic health check
curl http://127.0.0.1:7777/profile

# Check context
curl http://127.0.0.1:7777/context

# Check pending entries (if any)
curl http://127.0.0.1:7777/pending
```

## Lesson
When auditing an unknown local service:
- Always inspect the source code (search for `@app.route`, `Flask`, `FastAPI` decorators) before assuming endpoint names.
- If source not available, run `curl -v http://host:port/` to see available methods or check logs.
- Do not rely on conventional names; bridges often have custom minimal APIs.

## Related Skill
`systematic-debugging` Phase 1: Inspeccionar Servicios/Componentes Desconocidos