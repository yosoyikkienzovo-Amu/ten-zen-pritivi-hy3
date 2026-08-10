---
name: lm-studio-wsl-setup
description: Guía paso a paso para conectar Hermes (WSL) con LM Studio en Windows, resolviendo problemas de red y configuración.
---

# LM Studio + WSL Setup Guide

Skill para enlazar Hermes Agent (corriendo en WSL) con LM Studio (en Windows), incluyendo solución de problemas de red.

## Prerrequisitos
- LM Studio instalado en Windows
- WSL2 configurado
- Hermes Agent instalado en WSL

## Paso 1: Configurar LM Studio para aceptar conexiones externas
1. Abrir LM Studio → pestaña **Developer / Local Server**
2. Activar **"Permitir Conexiones de Red"** (o desmarcar "Bind to localhost only")
3. Verificar que escuche en `0.0.0.0:1234` (usar en PowerShell: `netstat -ano | findstr :1234`)
4. Reiniciar el servidor de LM Studio

## Paso 2: Abrir puerto en Firewall de Windows (crítico)
En PowerShell como Administrador:
```powershell
New-NetFirewallRule -DisplayName "WSL LM Studio" -Direction Inbound -LocalPort 1234 -Protocol TCP -Action Allow
```

## Paso 3: Obtener IP de Windows vista desde WSL
En terminal WSL:
```bash
WIN_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
echo "IP de Windows para WSL: $WIN_IP"
# Alternativamente, usar la IP de red local que muestra LM Studio (ej. 192.168.100.63)
```

## Paso 4: Probar conectividad desde WSL
```bash
# Probar con curl (debe devolver JSON con modelos)
curl --max-time 5 http://$WIN_IP:1234/v1/models
# Si falla, probar con la IP de red local de Windows
curl --max-time 5 http://192.168.100.63:1234/v1/models
```

## Paso 5: Configurar Hermes (config.yaml)
Editar `~/.hermes/config.yaml`:
```yaml
model:
  default: "mistralai/ministral-3-3b"  # Nombre exacto del modelo en LM Studio
  provider: "custom"
  extra:
    api_base: "http://IP_DE_WINDOWS:1234/v1"
    api_key: "sk-lm-XXXXXXXX"  # Token generado en LM Studio (si auth está activa)
```

## Paso 6: Configurar asistente auxiliar (opcional)
Para que compresión y títulos usen LM Studio local:
```yaml
auxiliary:
  compression:
    provider: "custom"
    extra:
      api_base: "http://IP_DE_WINDOWS:1234/v1"
      api_key: ""
  title_generation:
    provider: "custom"
    extra:
      api_base: "http://IP_DE_WINDOWS:1234/v1"
      api_key: ""
```

## Solución de problemas comunes
| Problema | Solución |
|-----------|-----------|
| `curl` timed out con IP WSL Gateway (`172.x.x.1`) | El gateway DNS de WSL no redirige al servicio en Windows. Probar con IP de red local que muestra LM Studio (ej. `192.168.100.63`). |
| `curl` timed out con IP de red local | Firewall de Windows puede estar bloqueando la subred de WSL. Verificar regla "WSL LM Studio" y asegurar que `Profile` sea "Any". |
| `host.docker.internal` no responde | En WSL2, este nombre puede no resolverse. Usar `netsh interface portproxy` como último recurso. |
| Modelo no encontrado | Usar nombre exacto que muestra `curl .../v1/models` (ej. `mistralai/ministral-3-3b`). |
| Error de autenticación (invalid_api_key / "An LM Studio API token is required") | 1. En LM Studio → pestaña Developer → "Manage Tokens", copia el token Bearer generado. 2. Agrega el token en `~/.hermes/config.yaml` bajo `model.extra.api_key` (o `auxiliary.compression.extra.api_key` / `auxiliary.title_generation.extra.api_key` para servicios auxiliares). 3. Para pruebas de conectividad, desactiva temporalmente "Require Authentication" en la configuración Developer de LM Studio para omitir la verificación de tokens. |
| **Conexión final Pendiente** | En esta sesión, no se logró conectar WSL → LM Studio a pesar de firewall abierto y `0.0.0.0:1234`. Próximo paso: Probar `netsh interface portproxy add v4tov4 listenport=1234 listenaddress=0.0.0.0 connectport=1234 connectaddress=127.0.0.1` en PowerShell (Admin) para reenviar tráfico de WSL al localhost de Windows. |

## Test-Time Compute (TTS) Integration
Use the `LMStudioClient` class (see `references/tts-lm-studio-client.md`) to enable deep reasoning via recursive Chain-of-Thought:
1. Initialize the client with `LMStudioClient(base_url="http://<WIN_IP>:1234/v1")`
2. Call `think_deep(prompt, reasoning_steps=N)` to generate N layers of recursive reasoning, where each step reflects on the previous output.
3. Use TTS for complex logic, code review, or security analysis tasks where deeper inference is required.

## Advanced Hybrid Architecture (OpenRouter + LM Studio)
TEN-ZEN should retain OpenRouter as primary identity (`model.default: tencent/hy3-preview:free`) and add LM Studio as secondary local layer for reasoning, TTS, embeddings, and memory. Configure `auxiliary`, `delegation`, and `mcp_servers` to point to LM Studio without overwriting OpenRouter settings.

### Honcho Self-Learning Loop Activation
Enable Honcho in `~/.hermes/config.yaml` to allow TEN-ZEN to auto-create skills from recurring LM Studio usage patterns:
```yaml
honcho:
  enabled: true
  auto_create_skills: true
  pattern_threshold: 3  # Create skill after 3 recurring uses
```

### Quantum Bridge Plugin (Hermes v0.5.0+ Lifecycle Hooks)
Create `quantum_bridge.py` plugin to intercept LLM calls via `pre_llm_call` hook, automatically route tasks to OpenRouter or LM Studio using dual-model voting:
1. Use `qwen2.5-0.5b-instruct@q8_0` as fast classifier (50ms latency)
2. Fallback to TEN-ZEN (OpenRouter) for uncertain classifications
3. Automatically activate TTS/deep reasoning for complex tasks

### Dual-Model Voting Routing
Implement two-judge classification:
- Judge 1: Local `qwen2.5-0.5b` (fast, 50ms)
- Judge 2: TEN-ZEN (OpenRouter) for second opinion on uncertain tasks
- Disagreements automatically trigger deep think mode

### JIT Model Loading (LM Studio 0.4.2+)
Only keep `qwen2.5-0.5b` permanently loaded in LM Studio; load larger models (e.g., `qwen2.5-coder-14b`, `deepseek-r1-qwen3-8b`) just-in-time when the arbiter requests them to save VRAM.

### MCP Server Setup (lmstudio_mcp_server.py)
Create `~/.hermes/mcp_servers/lmstudio_mcp_server.py` to expose LM Studio tools as MCP endpoints:
- `lmstudio_chat`: Chat with any loaded model
- `lmstudio_embed`: Generate local embeddings
- `lmstudio_reason`: Deep TTS reasoning
- `lmstudio_list_models`: List available models
Register in `config.yaml` under `mcp_servers`.

### think_deep Skill Configuration
Create `think_deep.yaml` skill for TEN-ZEN to consciously invoke deep reasoning:
```yaml
name: think_deep
description: Invoke LM Studio deep reasoning for complex tasks
trigger: ["necesito pensar mejor", "analiza profundamente", "razona paso a paso"]
steps:
  - Call lmstudio_reason MCP tool with task and depth=3
  - Return structured reasoning output
```

## Pitfalls
- **Style Compliance**: For all LM Studio tasks involving code, security, Windows system integrity, or hardening work, use standard professional zen tone. Only use k-style (bio-plasticidad lingüística) when Ikki explicitly invites you to play in a defined time window. Confusion between play/work styles can introduce errors that expose the system to external threats.
- **Model Loading**: The `think_deep` method simulates reasoning until a model is loaded in LM Studio; ensure a model is active in the LM Studio GUI/API before running production TTS tasks.
- **Authentication Errors**: If `curl http://<WIN_IP>:1234/v1/models` returns `invalid_api_key`, verify the token is correctly set in `config.yaml` or disable "Require Authentication" temporarily in LM Studio. Never commit API tokens to public repositories (e.g., Ten-Zen's GitHub repo).

## Comandos útiles
```bash
# Verificar proceso de LM Studio en Windows
tasklist | findstr lmstudio  # En PowerShell
# Verificar reglas de firewall
netsh advfirewall firewall show rule name="WSL LM Studio"  # PowerShell
# Reiniciar gateway de Hermes
hermes gateway restart
```
