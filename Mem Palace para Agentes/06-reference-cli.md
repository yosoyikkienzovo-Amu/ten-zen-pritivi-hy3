# MemPalace — Resumen 06: Reference/CLI

Fuente: https://mempalaceofficial.com/reference/cli.html
Última verificación: 2026-07-15

## 1. Comandos documentados oficialmente (11)
`init`, `mine`, `search`, `split`, `wake-up`, `compress`, `status`, `repair`, `mcp`, `hook`, `instructions`.
Todos aceptan `--palace <path>`; comando raíz acepta `--backend <name>`.

**Discrepancia registrada:** el binario real instalado (3.5.0) trae además `daemon`, `sweep`, `migrate`, `palace` — ninguno documentado en esta página oficial. `sweep` sí aparece mencionado en el README del repo (per-message recall, idempotente). Los otros 3 quedan sin documentación oficial encontrada — tratar con cautela, probar con `--dry-run`/`--help` antes de usar en el palace real.

## 2. Comandos clave
- `mempalace compress --wing myapp [--dry-run] [--config entities.json]` — AAAK. Ver 07-concepts-palace-aaak.md: NO USAR todavía, 12.4 puntos de regresión de recall, experimental.
- `mempalace repair` — reconstruye índice vectorial, backup automático en `<palace_path>.backup` antes de tocar nada.
- `mempalace status` — conteo de drawers + breakdown wing/room, sin argumentos.
- `mempalace hook run --hook {session-start|stop|precompact} --harness {claude-code|codex}` — dispara el guardado automático.
- `mempalace sweep <transcript-dir>` — un drawer verbatim por mensaje usuario/asistente, idempotente, resume-safe. Complementa los hooks (que trabajan a nivel de archivo).

## 3. Nota para otras instancias de IA
- Antes de usar `daemon`, `migrate`, `palace` (no documentados): correr `mempalace <comando> --help` primero y registrar lo que devuelva en este mismo archivo.
- `mempalace sweep` es el comando para llenar el hueco de "recall por mensaje individual" que los hooks de archivo completo no cubren.
