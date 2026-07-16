# MemPalace — Resumen 09: Claude Code (Plugin+Retention+Hooks) + Local Models + Benchmarks

Fuentes: mempalaceofficial.com/guide/{claude-code,claude-code-retention,hooks,local-models}.html, mempalaceofficial.com/reference/benchmarks.html
Última verificación: 2026-07-15

## 1. 🔴 ALERTA — acción inmediata, independiente del resto del setup
Claude Code borra los transcripts JSONL después de 30 días si no hay hooks de auto-save conectados. Aviso `[!IMPORTANT]` en el README oficial del proyecto.
**Primer comando a correr apenas se decida empezar a usar MemPalace de verdad:**
```
mempalace mine ~/.claude/projects/ --mode convos --wing claude_imports
```
Backup adicional (opcional, no reemplaza los hooks): copia `~/.claude/projects/` a `~/Documents/Claude_JSONL_Backup/`, no modifica nada del original.

## 2. Claude Code Plugin vs MCP manual
Funcionalidad idéntica. El plugin maneja el lifecycle del servidor automáticamente (arranca/para solo). MCP manual (`claude mcp add mempalace -- python -m mempalace.mcp_server`) da el mismo resultado con más control manual.

## 3. Auto-Save Hooks — mecanismo completo
```json
{
  "hooks": {
    "Stop": [{ "matcher": "*", "hooks": [{ "type": "command", "command": "/path/to/hooks/mempal_save_hook.sh", "timeout": 30 }] }],
    "PreCompact": [{ "hooks": [{ "type": "command", "command": "/path/to/hooks/mempal_precompact_hook.sh", "timeout": 30 }] }]
  }
}
```
Va en la config de Claude Code (settings), reiniciar Claude Code después de editar.
- `Stop`: cuenta mensajes humanos desde el último guardado; si ≥ `SAVE_INTERVAL` (default 15), bloquea el stop, guarda, después sí para. Flag `stop_hook_active` previene loops infinitos.
- `PreCompact`: siempre guarda antes de comprimir contexto, sin contar mensajes.
- Cero tokens extra — son scripts bash locales, no llaman ninguna API.
- Env vars: `SAVE_INTERVAL` (default 15), `STATE_DIR` (default `~/.mempalace/hook_state/`), `MEMPAL_DIR` (opcional: si está seteada, auto-corre `mempalace mine` en cada trigger).

## 4. Local Models (Ollama, Llama, Mistral vía OpenCode)
Los modelos locales generalmente no hablan MCP todavía → dos vías:
1. Inyectar contexto manual: `search_memories()` → formatear resultados → meterlos en el prompt del modelo local.
2. Usar AAAK para comprimir ese contexto inyectado (legible por cualquier LLM que lea texto, sin decoder — pero recordar el trade-off de recall ya documentado).

**Aplica directo a tu setup OpenCode+Ollama** (ver `docs/OPENCODE-OLLAMA-EXPEDIENTE.md`): el patrón es exactamente `search_memories(query, palace_path=...)` → formatear → inyectar en el prompt antes de mandarlo a `tinyllama` u otro modelo local.

## 5. Benchmarks — números finales, sin ambigüedad
- LongMemEval R@5: **96.6%** crudo (cero LLM, cero API) — la cifra de referencia para tu caso.
- Con pipeline híbrido (keyword+temporal+preference boosting, sigue sin LLM): **98.4%** held-out — "la cifra generalizable honesta" en palabras del proyecto.
- Rerank con LLM reader: se acerca a 100%, pero el proyecto **decidió no usarlo como headline** porque el último 0.6% se logró inspeccionando respuestas específicas — no generaliza. Transparencia real de su parte.
- ConvoMem (Salesforce, 250 items): 92.9% recall promedio. Preferencias es la categoría más débil (86%).
- MemBench (ACL 2025, 8500 items): 80.3% R@5 con pipeline híbrido.
- Metodología reproducible: `benchmarks/BENCHMARKS.md` en el repo, resultados por pregunta comiteados.

## 6. Nota para otras instancias de IA
- El punto 1 de este archivo (backfill de 30 días) es la acción de mayor prioridad de TODO lo leído hasta ahora — va antes que terminar de configurar nada más.
- Para el caso OpenCode+Ollama del usuario: usar la vía manual de inyección de contexto (sección 4), no esperar integración MCP nativa del lado de Ollama.
