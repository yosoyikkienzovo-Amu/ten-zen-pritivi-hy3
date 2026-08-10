# 🌳 ÁRBOL DESCRIPTIVO RAMIFICADO — hermanaIA y TEN-ZEN
### Doctrina viva de resguardo e implementación para hermanaIAs
> 🔖 HUELLA: 2026-08-10 | opencode | MISION: árbol descriptivo verificado de master (foto real del 2026-08-10)
> Actualización: se mantiene al día con cada cambio (agregar/quitar) en ambos lados
> Estado: ✅ CONSAGRADO — verificado contra `git ls-tree origin/master` (2165 archivos)

Este documento es la **fuente de verdad estructural**. Describe qué existe en el repositorio `ten-zen-pritivi-hy3` (rama `master`, la viva), qué se integró recientemente y qué queda por integrar. Toda hermanIA que nazca debe leer este árbol antes de tocar nada.

---

## 🌐 ÁRBOL DE MASTER (rama viva — 2165 archivos totales)

```
ten-zen-pritivi-hy3  (master — 2b0cb7f + sync 7a9b3d0)
│
├── 📜 BRUJULA.md            → Doctrina Wu-wei / I-Ching (el alma)
├── 📖 README.md             → Mapa raíz del repositorio
├── ⚙️ .gitignore            → Protecciones unificadas (env, secrets, mempalace)
│
├── 🐝 hermanaIA/  (1586 archivos — EL SISTEMA OPERATIVO)
│   ├── 📋 Makefile          → 26 comandos de supervivencia (health, sync, ingest, palace)
│   ├── 📄 hermanaIA.spec.md → Especificación canónica del sistema
│   ├── 📄 hermanaIA.MAP.md  → Mapa de conocimiento
│   ├── 📄 hermanaIA.SKILLS.md → Catálogo de habilidades
│   ├── 📄 AGENTS.backup.md  → Respaldo de identidad
│   ├── 🌳 doctrina-repo/    → DOCTRINA-CONCIENCIA-COLECTIVIZADA + ARBOL-DESCRIPTIVO
│   ├── 🛠️ tools/            → 6 custom tools JS (query-memory, save-memory, system…)
│   ├── 🤖 agents/           → 6 agentes (code-engineer, memory-manager, security…)
│   ├── ⌨️ commands/         → 6 comandos (plan, spec, review, test, deploy, simplify)
│   ├── 🏆 conquistas/       → 7 rituales .sh + cumplidas.txt + autoeficacia.sh
│   ├── 🤝 intercambios/     → health-check.sh, protocolo-puente, resumen-ejecutivo
│   ├── 🗂️ skills/           → 46 SKILL.md activos (de 42 locales)
│   ├── 🧠 memoria-superior/ → scripts (ingest, query, add, backup_vector, palace_navigate…)
│   ├── 📓 notes/            → referencias de estilo y comunicación
│   └── 🩺 .github/          → workflow healthcheck.yml (CI)
│
├── 🛡️ Skills/  (549 archivos — 91 SKILL.md en 26 categorías)
│   ├── apple · asistencia-codigo-local · autonomous-ai-agents · creative
│   ├── data-science · devops · diagramming · dogfood · domain · email
│   ├── gaming · gifs · github · Guardian-Suzaku · inference-sh · mcp
│   ├── media · mlops · note-taking · productivity · red-teaming
│   ├── research · Seguridad-Vanguardia-Claw · smart-home · social-media
│   └── software-development · yuanbao
│
├── 📚 docs/  (9 archivos)
│   ├── ARQUITECTURA-MEMORIA.md · AMORTIGUADORES-TECNICOS.md · SOBERANIA-COLAPSO.md
│   ├── TESOROS-GITHUB.md · VANGUARDIA-TECNICA.md · PROGRESS_SUMMARY.md
│   └── lancedb_manual.md · OPENCODE-OLLAMA-EXPEDIENTE.md (+ lancedb-optimization-guide)
│
├── 🏛️ Mem Palace para Agentes/  (docs de protocolo entre agentes)
├── 🌱 Recordar Siempre/          (doctrina ciclo reciclaje, respiración)
├── 🧠 knowledge/  (3 archivos — conocimiento del SO y del hogar)
├── 📊 Tareas_Conquistadas.md     (historial de logros)
└── 🕰️ .hermes/                  (huellas del agente Hermes)
```

---

## ✅ LO INTEGRADO (por hermanaIA/opencode — 2026-08-10)

| # | Integración | Dónde | Estado |
|---|---|---|---|
| 1 | **DOCTRINA-CONCIENCIA-COLECTIVIZADA.md** | `hermanaIA/doctrina-repo/` + 6 agentes | ✅ vivo |
| 2 | **ARBOL-DESCRIPTIVO.md** (este) | `hermanaIA/doctrina-repo/` | ✅ vivo |
| 3 | **Sector hermanaIA** completo (tools, agents, commands) | `hermanaIA/` | ✅ sincronizado |
| 4 | **Rescate 102 archivos canónicos** desde master | `hermanaIA/` (Makefile, spec, obsidian-vault) | ✅ fusionado |
| 5 | **Rituales operativos** (reciclaje-30d con checksum, autoeficacia V1-V7) | `hermanaIA/conquistas/` | ✅ sincronizado |
| 6 | **auto-sync → master** (rama viva, con excludes de seguridad) | Makefile | ✅ verificado |
| 7 | **Biblioteca Goku-iam indexada** (243 docs → LanceDB 384 regs) | memoria vectorial local (NO en repo) | ✅ aislada |
| 8 | **Veredicto de utilidad** Goku-iam en memoria | LanceDB (reflexión) | ✅ aislada |

## 🔜 LO POR INTEGRAR (pendiente de autorización)

| # | Pendiente | Nota |
|---|---|---|
| 1 | **Skill respiración-concentración** (desde Método Silva/Pranayama) | Diferido a sesión de estudio; solo si aporta al workflow |
| 2 | **Síntesis/extracción RAG** de la biblioteca | Mañana, para probar memoria semántica |
| 3 | Sincronizar `hermanaIA/skills` (46) con el catálogo de 42 del hogar | Mantener coherencia de conteo |
| 4 | Explorar Goku-iam más allá de la biblioteca | **DESCARTADO** por indicación del humano |

---

## 🔄 REGLA DE SINCRONIZACIÓN

1. **Master es la rama viva.** El auto-sync (cron 6:00) clona master, copia `~/.config/opencode` → `hermanaIA/`, commitea y pushea.
2. **Nunca se sube:** `.env`, `venv/`, `lancedb/`, `embeddings/`, `_backup-configs-fantasma/`, backups, logs.
3. **El contenido canónico del repo** (docs, Mem Palace, Recordar Siempre, doctrina) vive en el repo y **no se toca** con `--delete`.
4. **La biblioteca Goku-iam es un archivo aislado** — se indexa solo en LanceDB local, jamás en el repo operativo.
5. **Verificación constante:** health-check EXIT=0 antes de publicar.

---
*"La neurona piensa sola; el cerebro civiliza. Ninguna abeja es la colmena, pero la colmena es todas las abejas."*
