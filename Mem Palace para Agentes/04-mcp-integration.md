# MemPalace — Resumen 04: MCP Integration

Fuente: https://mempalaceofficial.com/guide/mcp-integration.html
Última verificación: 2026-07-13

## 1. Qué da
34 tools vía MCP → acceso read/write completo al palace desde cualquier cliente MCP-compatible.

## 2. Setup
```
mempalace mcp                                          # helper: imprime comando exacto
claude mcp add mempalace -- python -m mempalace.mcp_server
codex mcp add mempalace -- python -m mempalace.mcp_server
# con palace custom:
claude mcp add mempalace -- python -m mempalace.mcp_server --palace /path/to/palace
```

## 3. Compatibles
Claude Code (nativo/plugin), Codex CLI, OpenClaw (skill oficial), ChatGPT (bridge), Cursor (nativo), Gemini CLI.

## 4. Memory Protocol — política operativa obligatoria
Al llamar `mempalace_status` por primera vez, la IA recibe:
1. **Wake-up:** llamar `mempalace_status` → overview del palace.
2. **Antes de responder** sobre persona/proyecto/evento pasado: buscar primero, nunca adivinar.
3. **Si hay duda:** decir "déjame revisar" y consultar el palace.
4. **Después de cada sesión:** escribir diary entries (`mempalace_diary_write`).
5. **Cuando cambian hechos:** invalidar viejos (`mempalace_kg_invalidate`), agregar nuevos.

Esto es lo que convierte storage en memoria real: verificar antes de hablar, no alucinar.

## 5. Las 34 tools, por categoría

**Palace (lectura):** `mempalace_status`, `mempalace_list_wings`, `mempalace_list_rooms`, `mempalace_get_taxonomy`, `mempalace_search`, `mempalace_check_duplicate`, `mempalace_get_aaak_spec`

**Drawers (lectura):** `mempalace_get_drawer`, `mempalace_list_drawers`

**Palace (escritura):** `mempalace_add_drawer`, `mempalace_update_drawer`, `mempalace_delete_drawer`

**Knowledge Graph:** `mempalace_kg_query`, `mempalace_kg_add`, `mempalace_kg_invalidate`, `mempalace_kg_timeline`, `mempalace_kg_stats`

**Navegación:** `mempalace_traverse`, `mempalace_find_tunnels`, `mempalace_graph_stats`

**Tunnels:** `mempalace_create_tunnel`, `mempalace_list_tunnels`, `mempalace_delete_tunnel`, `mempalace_follow_tunnels`

**Agent Diary:** `mempalace_diary_write`, `mempalace_diary_read`

**Sistema:** `mempalace_hook_settings`, `mempalace_memories_filed_away`, `mempalace_reconnect`

Referencia detallada de schemas: `reference/mcp-tools.html` (pendiente de leer).

## 6. Nota para otras instancias de IA
- El protocolo de 5 pasos (sección 4) es **obligatorio**, no cosmético: define cuándo buscar, cuándo confesar incertidumbre, cuándo escribir diario.
- `mempalace_status` es la primera llamada de toda sesión — no `search` directo.
- Conceptos aún no resumidos que aparecen sin explicar: **AAAK** (dialecto/spec propio, ver `compress` y `get_aaak_spec`), **Knowledge Graph** (entidades/hechos con invalidación temporal, distinto de vector search), **Tunnels** (puentes explícitos entre wings). Pendiente: Concepts → The Palace, Knowledge Graph.
- Para 2 clientes (ej. Claude Desktop + Claude Code) sobre el mismo palace: mismo `--palace /path` en ambos `mcp add`, o dejar el default (`~/.mempalace/palace`) en los dos.
