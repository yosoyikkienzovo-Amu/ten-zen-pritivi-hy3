# MemPalace — Resumen 01: Getting Started

Fuente: https://mempalaceofficial.com/guide/getting-started.html
Última verificación: 2026-07-13

## 1. Qué es
Sistema de memoria local-first para IA. Recall 96.6% en benchmark LongMemEval. Cero llamadas a API para el flujo principal (corre localmente). Open source, MIT.

## 2. Instalación
1. Recomendado: `uv tool install mempalace` (entorno aislado, agrega `mempalace` al PATH).
2. Alternativa: `pip install mempalace`.
3. Desde código fuente:
   ```
   git clone https://github.com/MemPalace/mempalace.git
   cd mempalace
   uv sync --extra dev   # o: pip install -e ".[dev]"
   ```

## 3. ⚠️ Advertencia de seguridad crítica
`mempalace.tech` es un sitio de brand-squatting NO afiliado al proyecto. Corre ad-redirects y posible malware. Fuentes oficiales únicas:
- GitHub: https://github.com/MemPalace/mempalace
- PyPI: https://pypi.org/project/mempalace/

Nunca instalar binarios/scripts desde otros dominios.

## 4. Requisitos
- Python 3.9+
- `chromadb>=0.5.0` (auto-instalado)
- `pyyaml>=6.0` (auto-instalado)
- No requiere API key para el flujo local principal.

## 5. Quick Start — 3 pasos: init, mine, search

### Paso 1 — Inicializar el Palace
```
mempalace init ~/projects/myapp
# o desde dentro del proyecto:
mempalace init .
```
Qué hace:
- Detecta personas y proyectos por contenido de archivos
- Crea "rooms" (habitaciones) a partir de la estructura de carpetas
- Crea el directorio de config `~/.mempalace/`

### Paso 2 — Minar datos
```
mempalace mine ~/projects/myapp                          # código y docs
mempalace mine ~/chats/ --mode convos                     # exports de conversaciones
mempalace mine ~/chats/ --mode convos --extract general   # clasificación automática
```
Dos modos de minado + una estrategia de extracción:
- **projects** → código y docs, rooms auto-detectadas
- **convos** → exports de conversación (Claude, ChatGPT, Slack), fragmentados por par de intercambio
- **extract general** → clasifica contenido en: decisiones, preferencias, hitos (milestones), problemas, contexto emocional

### Paso 3 — Buscar
```
mempalace search "why did we switch to GraphQL"
```
Esto da un índice de memoria local funcional.

## 6. Qué pasa después del setup
No se vuelve a usar la CLI manualmente. La IA usa MemPalace automáticamente vía:
- Integración MCP
- Plugin de Codex (incluido)
- Plugin de Claude Code

Ejemplo de flujo: el usuario pregunta algo ("¿qué decidimos sobre auth el mes pasado?"), la IA llama a `mempalace_search` automáticamente, obtiene resultados verbatim, y responde. El comando `mempalace search` ya no se escribe a mano.

## 7. Siguientes páginas de la guía (pendientes de resumir)
1. Mining Your Data — profundización en modos de minado
2. Searching Memories
3. MCP Integration — conectar con Claude, Codex, ChatGPT, Cursor, Gemini
4. Claude Code Plugin
5. Claude Code Retention
6. Gemini CLI
7. Antigravity Plugin
8. OpenClaw Skill
9. Local Models
10. Auto-Save Hooks
11. Cursor IDE Hooks
12. Configuration
13. Remote / Team Server
14. Concepts → The Palace (wings, rooms, halls, tunnels)
15. Reference → CLI

## 8. Nota para otras instancias de IA que lean esto
- Los 3 comandos base son `init`, `mine`, `search`.
- El binario oficial solo viene de GitHub/PyPI — jamás de mempalace.tech.
- Una vez inicializado y minado, no hace falta invocar la CLI a mano: se usa vía MCP.
- Este archivo es el resumen 1 de N. Falta cubrir mining a fondo, MCP integration, y el concepto de "Palace" (wings/rooms/halls/tunnels) antes de considerar la documentación completa.
