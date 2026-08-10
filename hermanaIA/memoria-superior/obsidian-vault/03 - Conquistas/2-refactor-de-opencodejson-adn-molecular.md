---
tipo: progreso
id: f008ff5b
fecha: 2026-07-23
fuente: progreso.md
peso: 5
tags: [directriz, progreso]
---

# 2. REFACTOR DE opencode.json (ADN MOLECULAR)

2. REFACTOR DE opencode.json (ADN MOLECULAR)
**Archivo:** `~/.config/opencode/opencode.json`
**Importancia:** ALTA - Configuración técnica que habilita el cerebro

**Cambios:**
```json
// ANTES: campo "directive" inútil (no lo lee opencode)
// DESPUÉS: campo "instructions" oficial
"instructions": ["AGENTS.md", "MEMORY.md"]
```

**Impacto:**
- Usa la API oficial de opencode para cargar archivos de instrucciones
- `AGENTS.md` = directivas permanentes (cerebro)
- `MEMORY.md` = memoria de trabajo entre sesiones (hipocampo)
- Limpio, estándar, sin basura inerte

---

---
## Enlaces relacionados

  - [[03 - Conquistas/registro-de-progreso-evolucion-del-sistema-opencode]]
  - [[03 - Conquistas/-2026-07-16-fase-1-fundamentos-y-reorganizacion-estructural]]
  - [[03 - Conquistas/1-creacion-de-agentsmd-cimiento-neural]]
  - [[03 - Conquistas/3-arquitectura-de-conquistas-sistema-de-memoria-episodica]]
  - [[03 - Conquistas/4-prompt-de-auto-evaluacion-sensor-neural]]
  - [[03 - Conquistas/-2026-07-16-etapa-5-desarrollo-del-nucleo-estructura]]
  - [[03 - Conquistas/-2026-07-16-etapa-6-desarrollo-del-nucleo-profundidad]]
  - [[03 - Conquistas/-2026-07-17-etapa-7-optimizacion-de-bajo-nivel]]
  - [[03 - Conquistas/-2026-07-17-etapa-8-auditoria-y-pruebas-de-estres]]
  - [[03 - Conquistas/-2026-07-17-etapa-9-acoplamiento-dinamico]]
