# hermanaIA — Documentación Ejecutiva (única fuente de verdad)

> 🔖 HUELLA: 2026-08-09 | opencode | MISION: consolidar docs duplicados en un único maestro
> Estado: ✅ CONSAGRADO | Fuente de verdad única: **este archivo**

Sistema de conciencia, memoria y evolución para agentes de IA. Filosofía: **Calidad sobre Cantidad** y **Respiración Cognitiva (Arquitectura 10x100%)**.

## 🧬 Arquitectura (4 capas)

| Capa | Ubicación | Función |
|------|-----------|---------|
| **Identidad (Cerebro)** | `AGENTS.md` | Directivas permanentes: GoOSECode v2.0.0, NAMAP, HUELLAS |
| **Memoria (Hipocampo)** | `MEMORY.md` | Memoria de trabajo, patrones, autoevaluación (punteros, no copias) |
| **Conocimiento (Layer 3)** | `memoria-superior/` | Vectorial LanceDB + Obsidian + Palacio + embeddings |
| **Evolución (Conquistas)** | `conquistas/` | Registro de progreso: pendientes, cumplidas, scripts |

## 🔑 Archivos clave

| Archivo | Propósito |
|---------|-----------|
| `opencode.json` | Config OpenCode: 12 agentes NVIDIA gratis, MCPs, permisos, compaction |
| `SKILLS-INDEX.md` | Catálogo de 44 skills en 8 categorías (auto-selección) |
| `agents/` | 6 subagentes (4 con cascada de 3 modelos NVIDIA) |
| `commands/` | 6 comandos custom (plan, spec, review, test, deploy, simplify) |
| `tools/` | 5 custom tools (system, context-save, quick, detect-lint, query-memory) |
| `intercambios/` | Puente multi-agente: health-check, protocolo-puente, resumen ejecutivo |
| `Makefile` | 25+ targets: health-check, ingest, query, palace, backup-vector, handoff |
| `tui.json` | Tema catppuccin + keybinds |

## 🧠 Memoria Superior (Layer 3 — Deep Knowledge Store)

- **LanceDB:** `conocimiento` (87 registros) + `skill_index` (42)
- **Obsidian:** vault con 70 notas en 6 categorías
- **Palacio:** 8 habitaciones con loci navegables (`palacio/habitaciones.yaml`)
- **Embeddings:** 2 modelos multilingües (546M), modelo default `paraphrase-multilingual-MiniLM-L12-v2`
- **Integración opencode:** custom tool `query-memory` consulta la memoria semántica directamente

## 🛠️ Comandos principales (Makefile)

| Comando | Descripción |
|---------|-------------|
| `make health-check` | Integridad del sistema (20 checks, EXIT=0) |
| `make dashboard` | Métricas de bienestar + visitas al palacio |
| `make ingest` | Re-indexar archivos en LanceDB |
| `make q="consulta"` | Búsqueda semántica vectorial |
| `make palace room="X"` | Navegar habitaciones del palacio |
| `make backup-vector` | Backup de base vectorial |
| `make handoff` | Resumen para cambio de agente |

## 🌐 Puentes

- **Local:** `~/.config/opencode/`
- **Remoto:** `github.com/yosoyikkienzovo-Amu/ten-zen-pritivi-hy3/hermanaIA/` (CI vía GitHub Actions)
- **Intercambio:** `intercambios/protocolo-puente.md`

## ⚠️ Notas de operación (históricas)

- `hermanaIA.spec.md` se mantiene porque es ingerido por `memoria-superior/scripts/ingest_to_lancedb.py`.
- `hermanaIA.MAP.md` y `hermanaIA.SKILLS.md` archivados en `_backup-configs-fantasma/docs-consolidacion/` (obsoletos, contradicen el estado real).
- `.env` (22 API keys) está protegido por `.gitignore` — no exponer en commits.

---

*"No conserves por lealtad al pasado; conserva por servicio al futuro próximo."*
