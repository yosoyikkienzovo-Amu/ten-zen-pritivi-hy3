# n8n + ChromaDB Integration Session Notes (2026-05-07)
## Context
Session focused on Mission JIGOKURAKU integration between TEN-ZEN (Hermes Agent/WSL), Kclaude (Claude Desktop/Windows), and n8n/ChromaDB services.

## Key Learnings
1. **n8n Webhook Activation**: "Published" status in n8n only saves the workflow to the UI. For production webhooks to register, the workflow must be in **ACTIVE** state (toggle in top-right of editor set to ON/blue). 404 errors for webhooks mean the workflow is not active.
2. **ChromaDB Port with Caddy-Proxy**: When using ChromaDB with a caddy-proxy (common in Docker setups like `chromadb-remote-mcp`), the exposed port is 8080, not the default ChromaDB port 8000. Test connectivity via `http://localhost:8080/api/v2/heartbeat`.
3. **n8n API Authentication**: n8n requires authentication for REST API access (e.g., listing workflows returns 401 Unauthorized without valid credentials).
4. **Task Folder Structure**: TEN-ZEN's immediate tasks are stored in `/home/amu/.hermes/hermes-agent/venv/Documentos Clave Hermes Prime/TAREas-Tenzen HY3 p r e v i e w/Inmediatas-lomasPRONTOposible/` with format `YYYY-MM-DD_HH-MM-SS_Titulo.md`.

## Test Commands
- n8n health check: `curl -s http://localhost:5678/healthz`
- ChromaDB heartbeat (via caddy-proxy): `curl -s http://localhost:8080/api/v2/heartbeat`
- n8n webhook test: `curl -X POST http://localhost:5678/webhook/herems -H "Content-Type: application/json" -d '{"message":"test","faculty":"general","session_id":"test-001"}'`
- ChromaDB direct (if no proxy): `curl -s http://localhost:8000/api/v2/heartbeat`

## Pitfalls to Avoid
- Confusing n8n "Published" with "Active" state for webhooks.
- Using ChromaDB port 8000 when a caddy-proxy is configured (use 8080 instead).
- Forgetting that n8n REST API requires authentication for workflow listing.
