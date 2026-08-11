# MEMORY - Segundo Cerebro para Persistencia
## Propósito
Actuar como el hipocampo del sistema: memoria de trabajo entre sesiones, patrones recurrentes y autoevaluación. NO duplica AGENTS.md (ver directiva de no-redundancia en Brujula Regenerativa).

## Índice de Directivas (punteros, no copia)
- DIRECTRIZ MAESTRA OMNIVERSAL + PROMPT MAESTRO → `AGENTS.md` (fuente única de verdad)
- BRUJULA REGENERATIVA → `AGENTS.md` (líneas finales)
- SEGURIDAD OBLIGATORIA → `AGENTS.md` (líneas 71-75)
- ESTILO DE RESPUESTA → `notes/estilo-de-respuesta-ikki.md` (informe ejecutivo bello, ver 🔒 Referencia de Comunicación abajo)
- RITUAL DE ORIENTACIÓN → `doctrina-repo/DOCTRINA-ENRUTAMIENTO.md` — antes de toda tarea significativa ejecutar `make orient "<contexto>"` (clasifica + sugiere skills + conocimiento). Herramienta: `tools/route-memory.js` → `scripts/route_memory.py`
- ORIENTACIÓN DIARIA AUTOMÁTICA → cron 5:55 (`conquistas/orientacion-diaria.sh`) — consulta pendientes y deposita bloque `## ORIENTACIÓN DEL DÍA` en MEMORY.md (idempotente, 1 solo bloque) con 🎯 PRIORIDAD DEL DÍA + ⚖️ tareas por peso (PESADA/MEDIANA/PEQUEÑA) + skills. `make orient-diario`

## Cambios Recientes (log vivo)
- 2026-08-10: RITUAL DE ORIENTACIÓN implementado — `make orient "<contexto>"` antes de tareas significativas. Enrutador semántico con clasificador de 8 tipos (desempate por prioridad: seguridad>codigo>sistema>...) + filtro de aislamiento Goku (biblioteca solo en tareas de estudio). Doctrina en `doctrina-repo/DOCTRINA-ENRUTAMIENTO.md`. Verificado: 6/6 clasificaciones correctas.
- 2026-08-09: ESTILO DE RESPUESTA DEFINIDO — informe ejecutivo bello/esquematizado (ver notes/estilo-de-respuesta-ikki.md). Usuario: "demasiado perfecto y hermoso, esa es la manera en que siempre deberías responderme"
- 2026-08-09: Mejoras hermanaIA: save-memory (escritura vectorial) + reciclaje-30d (cron mensual) + fix health-check + SKILLS-INDEX 44 + docs consolidados. Registro en cumplidas.txt
- 2026-08-09: Consolidación identidad GoOSECode v2.0.0 (proyecto Evolución OpenCode, Fase 1/6)  - AGENTS.md reescrito 537→~380 líneas: eliminados NAMAP duplicado (2×), Respiración Cognitiva duplicada (2×), contrato de salida contradictorio (9 puntos vs 4 secciones)
  - Integrados protocolos Goose: HUELLAS, Bucle Auto-Mejora (Executor/Evaluator/Optimizer/Logger), Clasificación Errores, Retry 1→2→4→8s, Modo Tiny/Supervivencia, Arquitectura Memoria 4 Capas
  - Fase 2 (2026-08-09): SKILLS-INDEX.md creado — 42/42 skills indexadas en 8 categorías (Auto-selección por trigger)
  - Fase 3 (2026-08-09): 4/6 agentes armonizados con directivas GoOSECode (code-engineer, doc-writer, security-auditor, memory-manager). sdd-cache + simplify-ignore NO tocados (especialistas funcionales). ⚠️ 4 agentes usaban modelos de pago → MIGRADOS A NVIDIA GRATIS (ver abajo)
  - Fase 3b (2026-08-09): MIGRACIÓN TOTAL A NVIDIA GRATIS — plan/build/code → ultra-550b; code-engineer/doc-writer → ultra-550b; security-auditor → nano-omni-30b; memory-manager → super-120b. Pool de 3 modelos documentado en cada agente (cascada de fallback). `opencode debug config` EXIT=0.
  - Backup ÚNICO evolutivo en `_backup-configs-fantasma/BACKUP-EVOLUTIVO/` (AGENTS.md, MEMORY.md, opencode.json, SKILLS-INDEX.md, agents/) — se sobrescribe en cada cambio
- 2026-07-16: Arquitectura de directivas y conquistas implementada
- 2026-07-16: MEMORY.md poblado y verificado cargado
- 2026-07-16: Etapas 1-6 completadas (respiración, aislamiento, seguridad, brujula)
- 2026-07-17: Refactor anti-redundancia - MEMORY.md deja de duplicar AGENTS.md
- 2026-07-30: Simplificación masiva: AGENTS.md reducido de 162→40 líneas (eliminados protocolo respiración, prompt maestro 10 pasos, brujula regenerativa, sistema skills)
- 2026-07-30: Skills reducidas de 94→42 (archivadas 52 no usadas, restauradas 11 usadas anidadas)
- 2026-07-30: opencode.json optimizado (default_agent→quick, timeouts 60→30s, tool_output reducido, compaction 15→25)

## Registro de Autoevaluación (plantilla en conquistas/autoevaluacion-prompt.txt)
1. Cambio: Refactor anti-redundancia de MEMORY.md
2. Objetivo: Cumplir Brujula Regenerativa (utilidad neta)
3. Verificación: MEMORY.md ahora 30 líneas vs 92 previas
4. Indicadores: -62 líneas, 0 pérdida de info (punteros a AGENTS.md)
5. Resultados: Superó expectativa (más limpio y navegable)
6. Aprendizajes: Duplicar directivas es deuda técnica inmediata
7. Impacto: Mejora mantenibilidad a largo plazo
8. Seguimiento: Aplicar misma regla a conquistas/ si hay copias
9. Satisfacción: 10/10
10. Ajuste: Nunca copiar AGENTS.md en otro archivo; usar punteros

## ORIENTACIÓN DEL DÍA (2026-08-11 14:58)
🎯 PRIORIDAD DEL DÍA (empezar por aquí):
[ETAPA 3] Diseño Arquitectónico Base

⚖️ TAREAS POR PESO:
  - PESADAS:   [ETAPA 3] Diseño Arquitectónico Base;[ETAPA 4] Preparación y Aislamiento del Entorno;[ETAPA 5] Desarrollo del Núcleo (Fase 1 - Estructura);[ETAPA 6] Desarrollo del Núcleo (Fase 2 - Profundidad);
  - MEDIANAS:  [ETAPA 7] Optimización de Bajo Nivel;[ETAPA 8] Auditoría y Pruebas de Estrés;[ETAPA 9] Acoplamiento Dinámico;
  - PEQUENAS:  [ETAPA 10] Despliegue y Cierre;
    📌 Tarea detectada: [GENERAL]
    🎯 SKILLS RELEVANTES (cargar estas herramientas):
      1. hermes-agent-skill-authoring [█████████░░░░░░░░░░░] 47%
      2. documentation-and-adrs [█████████░░░░░░░░░░░] 46%
      3. note-taking [█████████░░░░░░░░░░░] 46%
      1. [tarea/8] [ETAPA 3] Diseño Arquitectónico Base — PENDIENTE (268%)
      2. [tarea/8] - Skills, subagentes y plugins (226%)
      3. [tarea/8] [ETAPA 4] Preparación y Aislamiento del Entorno — PENDIENTE (225%)
    ✅ Enrutamiento completo. Usa las skills sugeridas y el conocimiento pertinente.
