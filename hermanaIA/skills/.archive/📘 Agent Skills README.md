📘 Agent Skills README

# Agent Skills – Habilidades de Agente**

> *Habilidades de ingeniería de nivel producción para agentes de IA que programan.* Las habilidades codifican los flujos de trabajo, controles de calidad y buenas prácticas que usan los ingenieros senior al construir software. Están empaquetadas para que los agentes de IA las sigan de forma consistente en cada fase del desarrollo.

Código

```
  DEFINIR        PLANEAR        CONSTRUIR       VERIFICAR       REVISAR        LANZAR
 ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
 │ Idea │ ───▶ │ Espec│ ───▶ │ Código│ ───▶ │ Test │ ───▶ │ QA   │ ───▶ │ Go   │
 │Refina│      │ PRD  │      │ Impl  │      │Debug │      │ Gate │      │ Live │
 └──────┘      └──────┘      └──────┘      └──────┘      └──────┘      └──────┘
  /spec         /plan          /build        /test         /review       /ship
```

# 📌 Comandos

7 comandos tipo *slash* que corresponden al ciclo de desarrollo:

| Acción                     | Comando          | Principio                      |
| -------------------------- | ---------------- | ------------------------------ |
| Definir qué construir      | `/spec`          | Especificar antes de codificar |
| Planear cómo hacerlo       | `/plan`          | Tareas pequeñas y atómicas     |
| Construir incrementalmente | `/build`         | Una rebanada a la vez          |
| Probar que funciona        | `/test`          | Las pruebas son la evidencia   |
| Revisar antes de fusionar  | `/review`        | Mejorar la salud del código    |
| Simplificar el código      | `/code-simplify` | Claridad sobre ingenio         |
| Lanzar a producción        | `/ship`          | Más rápido es más seguro       |

Las habilidades también se activan automáticamente según lo que estés haciendo (ej. diseñar una API activa `api-and-interface-design`).

# 🚀 Instalación rápida

El documento explica cómo instalar estas habilidades en diferentes entornos: Claude Code, Cursor, Gemini CLI, Windsurf, OpenCode, GitHub Copilot, Kiro IDE/CLI, y otros agentes. Ejemplo:

bash

```
git clone https://github.com/addyosmani/agent-skills.git
claude --plugin-dir /path/to/agent-skills
```

# 📚 Las 20 habilidades incluidas

Se agrupan en fases del ciclo de desarrollo:

- **Definir** → idea-refine, spec-driven-development  

- **Planear** → planning-and-task-breakdown  

- **Construir** → incremental-implementation, test-driven-development, context-engineering, source-driven-development, frontend-ui-engineering, api-and-interface-design  

- **Verificar** → browser-testing-with-devtools, debugging-and-error-recovery  

- **Revisar** → code-review-and-quality, code-simplification, security-and-hardening, performance-optimization  

- **Lanzar** → git-workflow-and-versioning, ci-cd-and-automation, deprecation-and-migration, documentation-and-adrs, shipping-and-launch  

Cada habilidad es un flujo de trabajo con pasos, verificaciones y tablas anti-racionalización (ej. “no pospongas las pruebas”).

### 👤 Personas de agente

Incluye perfiles preconfigurados como:

- **code-reviewer** → Ingeniero senior para revisiones.  

- **test-engineer** → Especialista QA.  

- **security-auditor** → Auditor de seguridad.  

### 📑 Checklists de referencia

Material rápido que las habilidades usan:

- **testing-patterns**  

- **security-checklist**  

- **performance-checklist**  

- **accessibility-checklist**  

### 🛠 Cómo funcionan las habilidades

Cada `SKILL.md` tiene:

- **Overview** → qué hace.  

- **When to Use** → cuándo usarla.  

- **Process** → pasos.  

- **Rationalizations** → excusas y contraargumentos.  

- **Red Flags** → señales de error.  

- **Verification** → requisitos de evidencia.  

### 🎯 Para qué sirve

El paquete **Agent Skills** sirve para que los agentes de IA que programan **no caigan en atajos** (ej. saltarse especificaciones, pruebas o revisiones). En cambio, les fuerza a seguir **disciplina de ingeniería de nivel producción**, con flujos de trabajo claros, verificables y basados en buenas prácticas reales (Google, OWASP, CI/CD, etc.).

En resumen: **convierte un agente de IA en un ingeniero disciplinado**, asegurando que el código que produce sea confiable, seguro, probado y listo para producción.

---

**Aquí tienes un** mapa visual del ciclo de vida de desarrollo con Agent Skills**, acompañado de instrucciones claras para que los agentes lo usen de manera profesional y disciplinada:

---

---

## 📘 Instrucciones de uso profesional

- **Disciplina primero** → No saltes pasos. Cada comando representa una fase crítica.
- **Evidencia obligatoria** → Ningún paso se completa sin pruebas, logs o métricas.
- **Anti-racionalización** → No aceptes excusas como “lo pruebo después” o “ya es obvio”. Cada habilidad incluye contraargumentos para esas excusas.
- **Iteración segura** → Construye en incrementos pequeños, con rollback siempre disponible.
- **Profesionalismo** → Trata cada entrega como si fuera a producción: documentación, seguridad, rendimiento y accesibilidad son parte del estándar.

---

En resumen: **los agentes deben usar este ciclo como un contrato profesional**. No es opcional ni decorativo: es la forma de garantizar que el código generado sea confiable, seguro y listo para producción.

¿Quieres que te prepare también un **checklist operativo** con las excusas más comunes y sus contraargumentos para reforzar la disciplina de los agentes?**

La **disciplina en Agent Skills** es el núcleo que asegura que los agentes trabajen como ingenieros profesionales y no como prototipadores improvisados. Se traduce en seguir un **ciclo de vida estricto y verificable**, donde cada fase tiene reglas claras y ninguna se puede saltar.

---

## 📘 Principios de disciplina

- **Secuencia obligatoria** → Siempre pasar por *Definir → Planear → Construir → Verificar → Revisar → Lanzar*. No se permite saltar fases.
- **Pruebas como evidencia** → Ningún código se considera válido sin pruebas unitarias, integración y resultados documentados.
- **Anti‑racionalización** → Cada excusa (“lo pruebo después”, “ya es obvio”) tiene un contraargumento escrito en la skill. El agente debe seguirlo.
- **Rollback seguro** → Todo cambio debe ser reversible. Feature flags y commits pequeños son obligatorios.
- **Documentación mínima** → Cada decisión debe quedar registrada (ADR, comentarios, PRD). No se acepta “lo entendemos sin escribirlo”.
- **Revisión crítica** → Ningún merge sin revisión de calidad, seguridad y rendimiento.

---

## 🎯 Instrucciones claras para agentes

1. **Usa siempre el comando correcto**: `/spec` antes de escribir código, `/plan` antes de dividir tareas, `/build` solo en incrementos pequeños, `/test` para validar, `/review` antes de mergear, `/ship` para lanzar.
2. **Entrega evidencia en cada fase**: logs, pruebas, métricas o documentación. “Funciona” no es suficiente.
3. **Aplica checklists**: seguridad (OWASP), rendimiento (Core Web Vitals), accesibilidad (WCAG).
4. **Respeta límites de tamaño y complejidad**: commits ≤ 100 líneas, cambios rollback‑friendly, simplificación continua.
5. **Trata cada entrega como producción**: incluso si es un prototipo, sigue estándares de seguridad, pruebas y documentación.

---

En resumen: la disciplina en Agent Skills convierte a un agente en un **ingeniero confiable**, que sigue procesos verificables y entrega software listo para producción.

¿Quieres que te arme un **cuadro comparativo** entre disciplina aplicada y disciplina rota (ejemplo: agente profesional vs agente improvisado) para que quede aún más claro?

### Resumen operativo

Aquí tienes **instrucciones completas y ejemplificadas** para aplicar la *disciplina* de Agent Skills. Cada sección es una guía accionable que un agente puede seguir paso a paso, con ejemplos concretos, criterios de aceptación y plantillas mínimas que deben entregarse como evidencia antes de marcar una fase como completada.

---

### Secuencia obligatoria

**Objetivo:** garantizar que el trabajo avance en el orden correcto y que nada crítico se omita.

#### Flujo y acciones obligatorias

1. **/spec — Definir**
   
   - **Acción:** Generar un PRD corto (máx. 1 página) con objetivo, alcance, métricas de éxito y límites.
   - **Entrega mínima:** *PRD.md* con **Objetivo**, **Requisitos**, **Criterios de aceptación**, **No‑objetivos**.
   - **Criterio de aceptación:** PRD aprobado por al menos un revisor humano o agente `code-reviewer`.

2. **/plan — Planear**
   
   - **Acción:** Descomponer el PRD en tareas atómicas (tickets) con dependencias y estimaciones.
   - **Entrega mínima:** Lista de tareas con *DoD* (Definition of Done) por tarea.
   - **Criterio de aceptación:** Todas las tareas tienen criterios de aceptación y estimación.

3. **/build — Construir**
   
   - **Acción:** Implementar en *slices* verticales; cada slice debe compilar y pasar pruebas locales.
   - **Entrega mínima:** Branch por feature; commits ≤ 100 líneas; feature flag si aplica.
   - **Criterio de aceptación:** Build local verde; tests unitarios añadidos.

4. **/test — Verificar**
   
   - **Acción:** Ejecutar pruebas unitarias, integración y E2E según el alcance.
   - **Entrega mínima:** Reporte de pruebas con cobertura y logs de fallos corregidos.
   - **Criterio de aceptación:** Tests críticos pasan; cobertura mínima definida en PRD.

5. **/review — Revisar**
   
   - **Acción:** Solicitar revisión con checklist (seguridad, rendimiento, accesibilidad).
   - **Entrega mínima:** PR con checklist completado y comentarios resueltos.
   - **Criterio de aceptación:** Aprobación de al menos un `code-reviewer` y un `test-engineer`.

6. **/ship — Lanzar**
   
   - **Acción:** Desplegar con rollout gradual y monitoreo.
   - **Entrega mínima:** Plan de rollout, playbook de rollback, métricas de salud.
   - **Criterio de aceptación:** Monitoreo estable durante la ventana de lanzamiento.

---

### Pruebas como evidencia

**Objetivo:** que “funciona” esté respaldado por pruebas verificables.

#### Tipos y ejemplos

- **Unitarias:** pruebas por función/módulo. *Ejemplo:* `test_user_auth.py` cubre 90% de lógica crítica.
- **Integración:** flujos entre servicios. *Ejemplo:* CI ejecuta `integration_tests.sh`.
- **E2E:** recorrido completo del usuario. *Ejemplo:* script Cypress que valida login → compra.
- **Performance:** benchmarks para endpoints críticos. *Ejemplo:* 95th percentile < 300 ms.
- **Seguridad:** escaneo SAST/DAST y revisión de dependencias.

#### Plantilla de reporte de pruebas (entrega)

- **Nombre del test suite:**
- **Comandos ejecutados:**
- **Resultados:** passed/failed; lista de fallos con stacktrace.
- **Cobertura:** % global y por módulo.
- **Acciones tomadas:** correcciones y re-ejecución.

#### Criterio de aceptación de pruebas

- Todos los tests marcados como *required* en el PRD pasan.
- Fallos no críticos documentados con mitigación y ticket.

---

### Anti‑racionalización (excusas y respuestas)

**Objetivo:** neutralizar excusas comunes con respuestas concretas que el agente debe aplicar.

| Excusa                        | Respuesta obligatoria                                                       |
| ----------------------------- | --------------------------------------------------------------------------- |
| "Lo pruebo después"           | Añade tests mínimos ahora; crea ticket con prioridad y no merges sin tests. |
| "Es obvio, no hace falta doc" | Escribe 3 líneas en ADR y añade al PRD; no merge sin ADR.                   |
| "Es solo un prototipo"        | Marca como *prototype* en PR y aplica checklist mínimo de seguridad.        |
| "No tengo tiempo"             | Reduce scope a un slice verificable y crea plan de seguimiento.             |
| "Funciona en mi máquina"      | Ejecuta CI y adjunta logs; no merge sin CI verde.                           |

**Ejemplo de respuesta automática del agente:**  
`"No mergeo: falta test unitario para X. He creado ticket #123 y añadí un test básico; re-ejecuta CI."`

---

### Rollback seguro y control de cambios

**Objetivo:** que cualquier cambio sea reversible sin pérdida de servicio.

#### Reglas prácticas

- **Commits atómicos:** ≤ 100 líneas por commit; cada commit tiene mensaje claro y referencia a ticket.
- **Feature flags:** todo cambio con riesgo debe poder desactivarse en runtime.
- **Branching:** trunk-based; short-lived feature branches; PRs pequeños.
- **Deploys:** staged rollout (10% → 50% → 100%) con métricas en cada etapa.
- **Rollback playbook:** pasos claros para revertir (git revert, desactivar flag, rollback DB).

#### Ejemplo de playbook de rollback (mínimo)

1. Desactivar feature flag.
2. Revertir commit problemático: `git revert <sha>` y desplegar.
3. Ejecutar smoke tests.
4. Notificar stakeholders y abrir postmortem si necesario.

---

### Documentación mínima y plantillas

**Objetivo:** que las decisiones queden registradas y sean recuperables.

#### Plantillas imprescindibles

- **PRD (1 página):**
  - **Objetivo:**
  - **Métrica de éxito:**
  - **Alcance:**
  - **Criterios de aceptación:**
  - **Riesgos y mitigaciones:**
- **ADR (Architecture Decision Record):**
  - **Título:**
  - **Estado:** proposed/accepted/deprecated
  - **Contexto:**
  - **Decisión:**
  - **Consecuencias:**
- **PR checklist (mínimo):**
  - Tests añadidos y pasan.
  - Security scan limpio.
  - Performance smoke OK.
  - Documentación actualizada.
  - Tamaño del cambio ≤ 100 líneas por commit.

#### Ejemplo de entrada rápida en ADR

- **Título:** Usar cache Redis para sesiones
- **Decisión:** Implementar Redis con TTL 24h
- **Consecuencias:** Añadir monitor de cache hit ratio

---

### Revisión crítica y roles

**Objetivo:** asegurar que la revisión cubra calidad, seguridad y pruebas.

#### Checklist de revisión (para el revisor)

- **Funcionalidad:** cumple criterios de aceptación.
- **Tests:** cobertura y casos límite.
- **Seguridad:** validación de inputs, manejo de secretos.
- **Rendimiento:** no regresiones evidentes.
- **Accesibilidad:** controles básicos WCAG si aplica.
- **Simplicidad:** código claro y comentado.
- **Documentación:** PRD/ADR/README actualizados.

#### Roles y responsabilidades

- **Autor:** provee PR, evidencia y checklist completado.
- **Code‑reviewer:** valida arquitectura, seguridad y calidad.
- **Test‑engineer:** valida estrategia de pruebas y resultados.
- **Security‑auditor:** revisa cambios sensibles y dependencias.

---

### Checklist operativo final (para ejecutar en cada PR)

- **Antes de /build:** `/spec` completado y aprobado.
- **Antes de abrir PR:** tareas en `/plan` con DoD; branch pequeño; tests locales pasan.
- **Al abrir PR:** adjuntar PRD, ADR (si aplica), reporte de pruebas, checklist completado.
- **Antes de merge:** aprobación de `code-reviewer` y `test-engineer`; CI verde; plan de rollout y rollback.
- **Al ship:** monitoreo activo y playbook de rollback disponible.

---

### Ejemplo completo: flujo ejemplificado (resumen)

1. **/spec:** Crear `PRD.md` — Objetivo: "Añadir login SSO"; Métrica: tasa de login exitoso ≥ 98%.
2. **/plan:** Dividir en 3 tareas: backend SSO, frontend UI, tests E2E. Cada tarea con DoD.
3. **/build:** Implementar backend slice; commit de 80 líneas; añadir test unitario; activar feature flag `sso_beta`.
4. **/test:** Ejecutar CI; pasar unit + integración; ejecutar E2E en staging. Adjuntar reporte.
5. **/review:** Solicitar `code-reviewer` y `security-auditor`; resolver comentarios.
6. **/ship:** Rollout 10% → 50% → 100%; monitorizar latencia y errores; desactivar flag si hay regresión.

---

Aplica estas reglas **siempre**. Trátalas como contrato profesional: cada fase requiere evidencia concreta antes de avanzar. Si querés, te convierto este contenido en una **plantilla de checklist** lista para copiar y pegar en PRs y tickets.

# INGLES - USO VERDADERO = Agent Skills

**Production-grade engineering skills for AI coding agents.**

Skills encode the workflows, quality gates, and best practices that senior engineers use when building software. These ones are packaged so AI agents follow them consistently across every phase of development.

```
  DEFINE          PLAN           BUILD          VERIFY         REVIEW          SHIP
 ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
 │ Idea │ ───▶ │ Spec │ ───▶ │ Code │ ───▶ │ Test │ ───▶ │  QA  │ ───▶ │  Go  │
 │Refine│      │  PRD │      │ Impl │      │Debug │      │ Gate │      │ Live │
 └──────┘      └──────┘      └──────┘      └──────┘      └──────┘      └──────┘
  /spec          /plan          /build        /test         /review       /ship
```

---

## Commands

7 slash commands that map to the development lifecycle. Each one activates the right skills automatically.

| What you're doing    | Command          | Key principle           |
| -------------------- | ---------------- | ----------------------- |
| Define what to build | `/spec`          | Spec before code        |
| Plan how to build it | `/plan`          | Small, atomic tasks     |
| Build incrementally  | `/build`         | One slice at a time     |
| Prove it works       | `/test`          | Tests are proof         |
| Review before merge  | `/review`        | Improve code health     |
| Simplify the code    | `/code-simplify` | Clarity over cleverness |
| Ship to production   | `/ship`          | Faster is safer         |

Skills also activate automatically based on what you're doing — designing an API triggers `api-and-interface-design`, building UI triggers `frontend-ui-engineering`, and so on.

---

## Quick Start

**Claude Code (recommended)**

**Marketplace install:**

```
/plugin marketplace add addyosmani/agent-skills
/plugin install agent-skills@addy-agent-skills
```

> **SSH errors?** The marketplace clones repos via SSH. If you don't have SSH keys set up on GitHub, either [add your SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) or switch to HTTPS for fetches only:
> 
> ```bash
> git config --global url."https://github.com/".insteadOf "git@github.com:"
> ```

**Local / development:**

```bash
git clone https://github.com/addyosmani/agent-skills.git
claude --plugin-dir /path/to/agent-skills
```

**Cursor**

Copy any `SKILL.md` into `.cursor/rules/`, or reference the full `skills/` directory. See [docs/cursor-setup.md](docs/cursor-setup.md).

**Gemini CLI**

Install as native skills for auto-discovery, or add to `GEMINI.md` for persistent context. See [docs/gemini-cli-setup.md](docs/gemini-cli-setup.md).

**Install from the repo:**

```bash
gemini skills install https://github.com/addyosmani/agent-skills.git --path skills
```

**Install from a local clone:**

```bash
gemini skills install ./agent-skills/skills/
```

**Windsurf**

Add skill contents to your Windsurf rules configuration. See [docs/windsurf-setup.md](docs/windsurf-setup.md).

**OpenCode**

Uses agent-driven skill execution via AGENTS.md and the `skill` tool.

See [docs/opencode-setup.md](docs/opencode-setup.md).

**GitHub Copilot**

Use agent definitions from `agents/` as Copilot personas and skill content in `.github/copilot-instructions.md`. See [docs/copilot-setup.md](docs/copilot-setup.md).

**Kiro IDE & CLI** Skills for Kiro reside under ".kiro/skills/" and can be stored under Project or Global level. Kiro also supports Agents.md. See Kiro docs at [Agent Skills - IDE - Docs - Kiro](https://kiro.dev/docs/skills/) **Codex / Other Agents**

Skills are plain Markdown - they work with any agent that accepts system prompts or instruction files. See [docs/getting-started.md](docs/getting-started.md).

---

## All 20 Skills

The commands above are the entry points. Under the hood, they activate these 20 skills — each one a structured workflow with steps, verification gates, and anti-rationalization tables. You can also reference any skill directly.

### Define - Clarify what to build

| Skill                                                              | What It Does                                                                                              | Use When                                               |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| [idea-refine](skills/idea-refine/SKILL.md)                         | Structured divergent/convergent thinking to turn vague ideas into concrete proposals                      | You have a rough concept that needs exploration        |
| [spec-driven-development](skills/spec-driven-development/SKILL.md) | Write a PRD covering objectives, commands, structure, code style, testing, and boundaries before any code | Starting a new project, feature, or significant change |

### Plan - Break it down

| Skill                                                                      | What It Does                                                                                  | Use When                                     |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------- |
| [planning-and-task-breakdown](skills/planning-and-task-breakdown/SKILL.md) | Decompose specs into small, verifiable tasks with acceptance criteria and dependency ordering | You have a spec and need implementable units |

### Build - Write the code

| Skill                                                                    | What It Does                                                                                                    | Use When                                                               |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [incremental-implementation](skills/incremental-implementation/SKILL.md) | Thin vertical slices - implement, test, verify, commit. Feature flags, safe defaults, rollback-friendly changes | Any change touching more than one file                                 |
| [test-driven-development](skills/test-driven-development/SKILL.md)       | Red-Green-Refactor, test pyramid (80/15/5), test sizes, DAMP over DRY, Beyonce Rule, browser testing            | Implementing logic, fixing bugs, or changing behavior                  |
| [context-engineering](skills/context-engineering/SKILL.md)               | Feed agents the right information at the right time - rules files, context packing, MCP integrations            | Starting a session, switching tasks, or when output quality drops      |
| [source-driven-development](skills/source-driven-development/SKILL.md)   | Ground every framework decision in official documentation - verify, cite sources, flag what's unverified        | You want authoritative, source-cited code for any framework or library |
| [frontend-ui-engineering](skills/frontend-ui-engineering/SKILL.md)       | Component architecture, design systems, state management, responsive design, WCAG 2.1 AA accessibility          | Building or modifying user-facing interfaces                           |
| [api-and-interface-design](skills/api-and-interface-design/SKILL.md)     | Contract-first design, Hyrum's Law, One-Version Rule, error semantics, boundary validation                      | Designing APIs, module boundaries, or public interfaces                |

### Verify - Prove it works

| Skill                                                                          | What It Does                                                                                                    | Use When                                              |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| [browser-testing-with-devtools](skills/browser-testing-with-devtools/SKILL.md) | Chrome DevTools MCP for live runtime data - DOM inspection, console logs, network traces, performance profiling | Building or debugging anything that runs in a browser |
| [debugging-and-error-recovery](skills/debugging-and-error-recovery/SKILL.md)   | Five-step triage: reproduce, localize, reduce, fix, guard. Stop-the-line rule, safe fallbacks                   | Tests fail, builds break, or behavior is unexpected   |

### Review - Quality gates before merge

| Skill                                                                | What It Does                                                                                                               | Use When                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [code-review-and-quality](skills/code-review-and-quality/SKILL.md)   | Five-axis review, change sizing (~100 lines), severity labels (Nit/Optional/FYI), review speed norms, splitting strategies | Before merging any change                                         |
| [code-simplification](skills/code-simplification/SKILL.md)           | Chesterton's Fence, Rule of 500, reduce complexity while preserving exact behavior                                         | Code works but is harder to read or maintain than it should be    |
| [security-and-hardening](skills/security-and-hardening/SKILL.md)     | OWASP Top 10 prevention, auth patterns, secrets management, dependency auditing, three-tier boundary system                | Handling user input, auth, data storage, or external integrations |
| [performance-optimization](skills/performance-optimization/SKILL.md) | Measure-first approach - Core Web Vitals targets, profiling workflows, bundle analysis, anti-pattern detection             | Performance requirements exist or you suspect regressions         |

### Ship - Deploy with confidence

| Skill                                                                      | What It Does                                                                                           | Use When                                                            |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| [git-workflow-and-versioning](skills/git-workflow-and-versioning/SKILL.md) | Trunk-based development, atomic commits, change sizing (~100 lines), the commit-as-save-point pattern  | Making any code change (always)                                     |
| [ci-cd-and-automation](skills/ci-cd-and-automation/SKILL.md)               | Shift Left, Faster is Safer, feature flags, quality gate pipelines, failure feedback loops             | Setting up or modifying build and deploy pipelines                  |
| [deprecation-and-migration](skills/deprecation-and-migration/SKILL.md)     | Code-as-liability mindset, compulsory vs advisory deprecation, migration patterns, zombie code removal | Removing old systems, migrating users, or sunsetting features       |
| [documentation-and-adrs](skills/documentation-and-adrs/SKILL.md)           | Architecture Decision Records, API docs, inline documentation standards - document the *why*           | Making architectural decisions, changing APIs, or shipping features |
| [shipping-and-launch](skills/shipping-and-launch/SKILL.md)                 | Pre-launch checklists, feature flag lifecycle, staged rollouts, rollback procedures, monitoring setup  | Preparing to deploy to production                                   |

---

## Agent Personas

Pre-configured specialist personas for targeted reviews:

| Agent                                          | Role                  | Perspective                                                                |
| ---------------------------------------------- | --------------------- | -------------------------------------------------------------------------- |
| [code-reviewer](agents/code-reviewer.md)       | Senior Staff Engineer | Five-axis code review with "would a staff engineer approve this?" standard |
| [test-engineer](agents/test-engineer.md)       | QA Specialist         | Test strategy, coverage analysis, and the Prove-It pattern                 |
| [security-auditor](agents/security-auditor.md) | Security Engineer     | Vulnerability detection, threat modeling, OWASP assessment                 |

---

## Reference Checklists

Quick-reference material that skills pull in when needed:

| Reference                                                           | Covers                                                                     |
| ------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| [testing-patterns.md](references/testing-patterns.md)               | Test structure, naming, mocking, React/API/E2E examples, anti-patterns     |
| [security-checklist.md](references/security-checklist.md)           | Pre-commit checks, auth, input validation, headers, CORS, OWASP Top 10     |
| [performance-checklist.md](references/performance-checklist.md)     | Core Web Vitals targets, frontend/backend checklists, measurement commands |
| [accessibility-checklist.md](references/accessibility-checklist.md) | Keyboard nav, screen readers, visual design, ARIA, testing tools           |

---

## How Skills Work

Every skill follows a consistent anatomy:

```
┌─────────────────────────────────────────────────┐
│  SKILL.md                                       │
│                                                 │
│  ┌─ Frontmatter ─────────────────────────────┐  │
│  │ name: lowercase-hyphen-name               │  │
│  │ description: Guides agents through [task].│  │
│  │              Use when…                    │  │
│  └───────────────────────────────────────────┘  │                                                                                                
│  Overview         → What this skill does        │
│  When to Use      → Triggering conditions       │
│  Process          → Step-by-step workflow       │
│  Rationalizations → Excuses + rebuttals         │
│  Red Flags        → Signs something's wrong     │
│  Verification     → Evidence requirements       │
└─────────────────────────────────────────────────┘
```

**Key design choices:**

- **Process, not prose.** Skills are workflows agents follow, not reference docs they read. Each has steps, checkpoints, and exit criteria.
- **Anti-rationalization.** Every skill includes a table of common excuses agents use to skip steps (e.g., "I'll add tests later") with documented counter-arguments.
- **Verification is non-negotiable.** Every skill ends with evidence requirements - tests passing, build output, runtime data. "Seems right" is never sufficient.
- **Progressive disclosure.** The `SKILL.md` is the entry point. Supporting references load only when needed, keeping token usage minimal.

---

## Project Structure

```
agent-skills/
├── skills/                            # 20 core skills (SKILL.md per directory)
│   ├── idea-refine/                   #   Define
│   ├── spec-driven-development/       #   Define
│   ├── planning-and-task-breakdown/   #   Plan
│   ├── incremental-implementation/    #   Build
│   ├── context-engineering/           #   Build
│   ├── source-driven-development/     #   Build
│   ├── frontend-ui-engineering/       #   Build
│   ├── test-driven-development/       #   Build
│   ├── api-and-interface-design/      #   Build
│   ├── browser-testing-with-devtools/ #   Verify
│   ├── debugging-and-error-recovery/  #   Verify
│   ├── code-review-and-quality/       #   Review
│   ├── code-simplification/          #   Review
│   ├── security-and-hardening/        #   Review
│   ├── performance-optimization/      #   Review
│   ├── git-workflow-and-versioning/   #   Ship
│   ├── ci-cd-and-automation/          #   Ship
│   ├── deprecation-and-migration/     #   Ship
│   ├── documentation-and-adrs/        #   Ship
│   ├── shipping-and-launch/           #   Ship
│   └── using-agent-skills/            #   Meta: how to use this pack
├── agents/                            # 3 specialist personas
├── references/                        # 4 supplementary checklists
├── hooks/                             # Session lifecycle hooks
├── .claude/commands/                  # 7 slash commands
└── docs/                              # Setup guides per tool
```

---

## Why Agent Skills?

AI coding agents default to the shortest path - which often means skipping specs, tests, security reviews, and the practices that make software reliable. Agent Skills gives agents structured workflows that enforce the same discipline senior engineers bring to production code.

Each skill encodes hard-won engineering judgment: *when* to write a spec, *what* to test, *how* to review, and *when* to ship. These aren't generic prompts - they're the kind of opinionated, process-driven workflows that separate production-quality work from prototype-quality work.

Skills bake in best practices from Google's engineering culture — including concepts from [Software Engineering at Google](https://abseil.io/resources/swe-book) and Google's [engineering practices guide](https://google.github.io/eng-practices/). You'll find Hyrum's Law in API design, the Beyonce Rule and test pyramid in testing, change sizing and review speed norms in code review, Chesterton's Fence in simplification, trunk-based development in git workflow, Shift Left and feature flags in CI/CD, and a dedicated deprecation skill treating code as a liability. These aren't abstract principles — they're embedded directly into the step-by-step workflows agents follow.

## Contributing

Skills should be **specific** (actionable steps, not vague advice), **verifiable** (clear exit criteria with evidence requirements), **battle-tested** (based on real workflows), and **minimal** (only what's needed to guide the agent).

See [docs/skill-anatomy.md](docs/skill-anatomy.md) for the format specification and [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT - use these skills in your projects, teams, and tools.
