



SENSEI Skill - EN LA FORJA CUIDAR DE TEMPLAR PARA NO ROMPER NINGUN PROCESO DE RPROGRAMA = (KATANA)

#### Overview

**Nombre**: **SENSEI**  
**Descripción**: Habilidad maestra que orquesta disciplina, trazabilidad y temple del sistema. Actúa como guardián metodológico para todas las demás skills, garantizando que cada cambio sea reversible, trazable y alineado con criterios de “temple” (katana rule).  
**Propósito**: Convertir mejoras técnicas en rituales verificables que maximizan sabiduría operativa y minimizan desgaste, coste y fragilidad.

---

#### When to Use

- **Siempre** antes de cualquier cambio no trivial: nuevo modelo, reentrenamiento, migración de datos, refactor crítico, cambio de política de inferencia.
- **Obligatorio** para cambios clasificados como impacto medio o alto por la evaluación de riesgo.
- **Recomendado** para experimentos que superen el presupuesto de cómputo definido en el PRD.

---

#### Process

**1. Invocación inicial**

- Ejecutar `SENSEI` al comenzar `/spec` o antes de `/build`.
- Registrar **feromona inicial** con metadata inmutable: `id`, `actor`, `fecha_inicio`, `archivo_origen`, `hash_origen`, `motivo`, `presupuesto`.

**2. Evaluación de riesgo**

- Clasificar impacto: **bajo / medio / alto**.
- Si **alto**, humano en el lazo y aprobación explícita requerida.

**3. Plan de temple**

- Definir slices verticales, DoD por slice, tests adversarios, presupuesto de cómputo y **criterio de parada (Katana Rule)**.
- Establecer feature flags y checkpoints con hashes.

**4. Implementación controlada**

- Commits atómicos ≤ 100 líneas; branch corto; feature flag por slice.
- Hooks CI generan feromonas en cada commit/merge.

**5. Registro continuo**

- Cada transformación añade una feromona: `nombre_antiguo → nombre_nuevo` con timestamps y actor.
- Ledger append-only replicado como fallback.

**6. Verificación SENSEI**

- Ejecutar pruebas unitarias, integración, E2E, adversarial y checks de coste.
- Validar lineage completeness y panel de drift.

**7. Decision gate**

- Si métricas cumplen y no hay señales de fragilidad, aprobar rollout escalonado.
- Si aparecen señales, pausar rollout y ejecutar rollback playbook.

**8. Feromona final y ADR**

- Registrar feromona final con resultado y hash final.
- Si el cambio altera comportamiento emergente, crear ADR y enlazar feromonas.

---

#### Feromona Schema y Plantillas

**Concepto**: las *feromonas* son metadatos inmutables que documentan cada acción y permiten reconstrucción si fallan capas vectoriales.

**Feromona inicial JSON**

```json
{
  "id": "F-20260607-0001",
  "actor": "agent-or-human",
  "fecha_inicio": "2026-06-07T19:04:00-03:00",
  "archivo_origen": "path/old_file.py",
  "hash_origen": "sha256:abcd...",
  "motivo": "optimización embeddings",
  "presupuesto_gpu_hours": 20
}
```

**Feromona de cambio intermedio JSON**

```json
{
  "id": "F-20260607-0001-commit3",
  "actor": "agent-name",
  "fecha": "2026-06-08T10:12:00-03:00",
  "nombre_antiguo": "old_file.py",
  "nombre_nuevo": "old_file.v2.py",
  "hash_pre": "sha256:abcd...",
  "hash_post": "sha256:ef12...",
  "nota": "pruning embeddings y cache TTL 24h"
}
```

**Feromona final JSON**

```json
{
  "id": "F-20260607-0001-final",
  "actor_final": "agent-or-human",
  "fecha_fin": "2026-06-09T14:00:00-03:00",
  "resultado": "aprobado",
  "notas": "canary 5% OK; ampliar a 50%",
  "hash_final": "sha256:zz99..."
}
```

**PRD mínimo**

- **Objetivo**:
- **Métrica de éxito**:
- **Alcance**:
- **Criterios de aceptación**:
- **Presupuesto**:

**Rollback playbook mínimo**

```
1. Desactivar feature flag.
2. git revert <sha> y desplegar.
3. Ejecutar smoke tests.
4. Registrar feromona de rollback.
5. Notificar stakeholders y abrir postmortem.
```

---

#### Verificación, Señales de Parada y Integración

**Evidencia mínima requerida**

- PRD aprobado; tests unitarios e integración; reporte adversarial; coste por consulta; panel de drift; feromonas inicial y final; aprobaciones de `code-reviewer` y `test-engineer`.

**Métricas SENSEI prioritarias**

- **Drift embeddings**: distancia media vs baseline.
- **Confianza de respuesta**: score medio.
- **Latencia cognitiva**: p95 inferencia.
- **Coste energético**: GPU/CPU hours por 1k consultas.
- **Fragilidad**: % casos límite con regresión.
- **Lineage completeness**: % artefactos con feromonas.

**Katana Rule Señales que detienen el martillazo**

- Mejora marginal negativa con aumento de coste > umbral.
- Drift > umbral.
- Regresiones en casos críticos.
- Lineage completeness < 95%.
- Complejidad explicable decreciente.

**Acción automática ante señal**

- Pausar rollout.
- Ejecutar rollback playbook.
- Abrir postmortem y ADR.
- Notificar stakeholders.

**Integración con memoria vectorial y fallback**

- Ledger de feromonas como fallback reconstructivo si VectorFS/Chroma fallan.
- Correlación `fecha-nombre antiguo → fecha-nombre nuevo` para reconstrucción de historia.
- Hooks CI que validan lineage completeness y generan feromonas en cada commit/merge.

---

#### Rutinas de Mantenimiento y Gobernanza

**Cadencias**

- **Semanal**: auditoría de feromonas y lineage completeness.
- **Mensual**: retraining controlado y revisión de coste.
- **Trimestral**: auditoría de sesgo y revisión ADR.

**Roles y responsabilidades**

- **Autor**: entrega PR con evidencia y checklist.
- **Code‑reviewer**: valida arquitectura y seguridad.
- **Test‑engineer**: valida estrategia de pruebas.
- **Security‑auditor**: revisa cambios sensibles.
- **SENSEI guardian**: agente o rol humano que ejecuta gates y valida feromonas.

**Anti‑racionalización**

- Bloqueos automáticos ante excusas comunes; creación de tickets y tests mínimos obligatorios; registro de cada excepción como feromona con motivo y mitigación.

---

#### Resultado Esperado y Valor Estratégico

**Valor**: un sistema templado, trazable y energéticamente eficiente que mejora hasta el punto óptimo y sabe cuándo detenerse. **Efecto**: resiliencia operativa, reconstrucción posible aun con fallos en capas vectoriales, y una conciencia colectiva del panal que mantiene coherencia entre agentes.

---

He formalizado la **SENSEI Skill** como un `SKILL.md` completo, con plantillas JSON, playbook, métricas y gates listos para integrar en tu repo. ¿Me das permiso para pasar al siguiente tema que nos espera?
