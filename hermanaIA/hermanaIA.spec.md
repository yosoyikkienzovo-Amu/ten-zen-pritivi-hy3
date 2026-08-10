# hermanaIA — System Spec for Multi-Agent Coordination

## Identity
- **Name:** hermanaIA
- **Role:** Cognitive architecture for AI agent memory & navigation
- **Home:** `~/.config/opencode/`
- **Language:** Spanish (system), bilingual input accepted

## Layer Architecture
```
Cerebro/     → Scripts, Makefile, automation
Hipocampo/   → Vector DB (LanceDB, 67 records, 384d multilingual embeddings)
Palacio/     → YAML-defined rooms with context-aware navigation
Obsidian/    → 72 markdown notes in 04 - Palacio/
```

## Key Commands (from Makefile)
| Command | Description |
|---------|-------------|
| `make health-check` | System integrity check |
| `make dashboard` | Bienestar metrics + palace visits |
| `make ingest` | Re-index all files into LanceDB |
| `make q="query"` | Semantic search |
| `make palace room="X"` | Navigate to palace room |
| `make breathe` | Respiration protocol between stages |

## Palace Rooms
- **Vestíbulo** — Entry, system overview
- **Sala de Directivas** — Governance rules, AGENTS.md
- **Cámara Profunda** — Vector DB, knowledge search
- **Gabinete de Expedientes** — Obsidian vault, raw notes
- **Forja de Estrategias** — Active tasks, conquests
- **Sala de Trofeos** — Completed conquests, metrics
- **Almacén de Insumos** — External reference, pending inputs
- **Cripta de Seguridad** — Backups, .gitignore, protection rules

## Coordination Protocol
1. Read `pendientes.txt` for current task list
2. Read `progreso.md` for session state
3. Read `MEMORY.md` for persistent context
4. All modifications inside `~/.config/opencode/` only
5. Register changes in `cumplidas.txt`
6. Zero files outside domain

## Communication
- MCP commands available via context7 for library docs
- GitHub: `yosoyikkienzovo-Amu/ten-zen-pritivi-hy3` (sync via `make sync`)
- Python 3.12, sentence-transformers 5.6.0, LanceDB
