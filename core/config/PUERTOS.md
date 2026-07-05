# 🏠 Registro de Territorio: Mapa de Puertos y Servicios (v2.0)

Este documento es la **Ley de Convivencia** para todas las IAs y servicios en el ecosistema TEN-ZEN. Antes de levantar cualquier servicio, es obligatorio consultar y registrar el puerto aquí para evitar colisiones y retrocesos.

## 📜 Reglas de Oro
1. **Consultar antes de actuar:** Ninguna IA debe usar un puerto que no esté libre en esta lista.
2. **Registro Obligatorio:** Si una IA asigna un puerto nuevo, debe actualizar este archivo inmediatamente.
3. **Verificación Viva:** Este mapa se verifica y actualiza constantemente. Si una hermanaIA detecta un error o un servicio caído, debe reportarlo y buscar la solución de inmediato.
4. **Red WSL-Windows:** 
    - Desde WSL hacia Windows: usar `host.docker.internal` o `192.168.1.173`.
    - Desde Windows hacia WSL: `localhost` funciona.

## 📍 Mapa de Puertos - El Templo

| Puerto | Servicio | OS | Estado | URL desde WSL |
| :--- | :--- | :--- | :--- | :--- |
| **3000** | chroma-mcp-server | Windows | Docker Healthy | Interno |
| **4000** | LiteLLM proxy | WSL | OPERATIVO (systemd) | http://localhost:4000 |
| **5000** | MLflow | Windows | Docker running | http://host.docker.internal:5000 |
| **5432** | PostgreSQL dragon | Windows | Docker running | host.docker.internal:5432 |
| **5678** | n8n | Windows | Docker running | http://host.docker.internal:5678 |
| **7000** | Odysseus | Windows | Docker running | http://host.docker.internal:7000 |
| **7777** | Memory Bridge | WSL | Activo | http://localhost:7777 |
| **8000** | ChromaDB MP | Windows | Restart pendiente | http://host.docker.internal:8000 |
| **8080** | SearXNG | Windows | Docker (Odysseus) | http://host.docker.internal:8080 |
| **8091** | ntfy | Windows | Docker (Odysseus) | http://host.docker.internal:8091 |
| **8100** | ChromaDB Odysseus | Windows | Docker running | Solo Odysseus |
| **11434** | Ollama | Windows | Manual al login | http://host.docker.internal:11434 |
| **18789** | OpenClaw gateway | Windows | Running | http://host.docker.internal:18789 |
| **27123** | Obsidian REST | Windows | Portproxy OK | http://host.docker.internal:27123 |
| **1234** | LM Studio | Windows | NO corriendo | http://host.docker.internal:1234 |

## 🧠 LiteLLM Fallback (Orden Automático)
1. **Tier 1:** Ollama `qwen3:8b` (Local)
2. **Tier 2:** LM Studio (Local - Inactivo)
3. **Tier 3:** Groq `llama-3.3-70b` (Operativo)
4. **Tier 4:** OpenRouter free
5. **Tier 5:** Claude Haiku

## 📜 Credenciales y Notas
- **n8n LiteLLM:** `sk-templo-ikki-2026` | Base: `http://localhost:4000/v1`
- **OpenClaw Token:** `d6f6417e2cbc95ebb32ace011410d1d52d206ce846496766`
- **Ollama Modelos:** `qwen3:8b`, `deepseek-r1:8b`, `phi4-mini-reasoning`, `nomic-embed-text`.

---
*Cualquier discrepancia detectada por una hermanaIA debe ser corregida para mantener la lucidez monumental.*
