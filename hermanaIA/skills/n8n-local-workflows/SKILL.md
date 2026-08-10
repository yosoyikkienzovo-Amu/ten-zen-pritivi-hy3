---
name: n8n-local-workflows
description: Manage n8n workflows for local AI stacks (Ollama, LM Studio, ChromaDB), including deployment via REST API/PowerShell, webhook configuration, and Cloudflare tunnel integration.
trigger:
  - Deploying or updating n8n workflows for local self-hosted AI stacks
  - Configuring n8n webhooks to interface with local LLMs or vector databases
  - Integrating n8n with Cloudflare tunnels for public access
  - Managing n8n workflow lifecycle (import, activate, delete stale workflows)
---

# n8n Local Workflow Management

## Key Facts
- CCC project workflow "CCC Hermes Agent v5.2 FIXED" uses webhook path `hermes` (not `herems`); if fails, test fallback `herems` per user instruction
- n8n runs in Docker, accessible via `localhost:5678` on Windows host; WSL accesses via `localhost:5678`, Windows host IP (e.g., 192.168.1.174) times out from WSL
- Deployment uses PowerShell scripts with n8n REST API (import, activate, cleanup)
- Webhook 404/empty response usually indicates workflow is not ACTIVE, not path mismatch

## Welcome Protocol (Protocolo de Bienvenida)
- Sistema multi-agente coordinado; ningún agente ve todo solo.
- Coordinación ocurre mediante:
  1) n8n como bus central
  2) webhooks como protocolo universal
  3) ChromaDB como memoria vectorial compartida
  4) este documento (el skill o notas de sesión) como contexto base
- Reglas:
  * Verificar health check antes de acceder a servicios
  * Reportar modificaciones críticas, scripts y outputs en Temp (nunca usar PowerShell directo para capturar stdout - Yuzuriha)
  * Webhook de HERMES como vía principal para dejar mensajes
  * Contacto con Claude: compartir documento al inicio de sesión para "recordarle" contexto; comunicación en tiempo real vía n8n webhook + ChromaDB

## Deployment Steps (Windows PowerShell)
1. Verify n8n health: `Invoke-WebRequest "http://localhost:5678/healthz" -UseBasicParsing`
2. Read workflow JSON: `$workflowJson = Get-Content "CCC_n8n_HermesAgent_v5.2_FIXED.json" -Raw -Encoding UTF8`
3. Authenticate with n8n API key (set `$env:N8N_API_KEY` or input manually)
4. Clean existing Hermes/CCC workflows: `Invoke-RestMethod "$n8nUrl/api/v1/workflows" -Headers $headers`
5. Import workflow: `POST $n8nUrl/api/v1/workflows` with JSON body
6. Activate workflow: `PATCH $n8nUrl/api/v1/workflows/{id}` with `{"active": true}`
7. Test webhook: `POST http://localhost:5678/webhook/hermes`

## WSL Testing Steps
Use these steps when testing n8n from WSL instead of Windows PowerShell:
1. Verify n8n health: `curl -s -o /dev/null -w "%{http_code}" http://localhost:5678/healthz` (expect 200)
2. Test webhook with JSON-defined path first: `curl -X POST http://localhost:5678/webhook/hermes -H "Content-Type: application/json" -d '{"message":"test","faculty":"general","session_id":"wsl-test"}' --max-time 60`
3. If fails, test user-corrected fallback path: `curl -X POST http://localhost:5678/webhook/herems ...`
4. If 404 persists, confirm workflow is ACTIVE in n8n UI (toggle ON, blue)

## Common Pitfalls
- Workflow not active: 404 on webhook URLs almost always means the workflow is not toggled ON (blue) in n8n UI, regardless of path correctness. Check activation status FIRST before debugging paths.
- Webhook path fallback: If `hermes` path fails, test `herems` as per user instruction.
- WSL-Windows connectivity: WSL cannot reach n8n via Windows host IP (e.g., 192.168.1.174) due to timeouts; use `localhost:5678` in WSL if Docker port mapping is correct (0.0.0.0:5678->5678/tcp).
- n8n API auth: All n8n API requests (including listing workflows) require `X-N8N-API-KEY` header. If unavailable from WSL, use Windows PowerShell deploy script instead.
- Cloudflare tunnel URL changes on restart: Update Hermes config.yaml with new URL

## References
- `scripts/CCC_DEPLOY.ps1`: Automated deployment script for Windows PowerShell, WSL path: `/mnt/c/Users/Ikki/Downloads/06_Archivos/ULTIMOS KLAUDE N8N TENZEN INTERCONEXION 1/files-KLAUDE 2/CCC_DEPLOY .ps1`
- `templates/CCC_n8n_HermesAgent_v5.2_FIXED.json`: Base workflow template, WSL path: `/mnt/c/Users/Ikki/Downloads/06_Archivos/ULTIMOS KLAUDE N8N TENZEN INTERCONEXION 1/files-KLAUDE 2/CCC_n8n_HermesAgent_v5.2_FIXED.json`
