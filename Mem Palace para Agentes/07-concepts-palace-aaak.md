# MemPalace — Resumen 07: Concepts — The Palace + AAAK Dialect

Fuentes: https://mempalaceofficial.com/concepts/the-palace.html, https://mempalaceofficial.com/concepts/aaak-dialect.html
Última verificación: 2026-07-15

## 1. Jerarquía completa (corrige/amplía resumen 01 de "Palacio de la Memoria Amú Judár")
```
WING (persona/proyecto)
  └── HALL (categoría: hall_facts, hall_events, hall_discoveries, hall_preferences, hall_advice)
        └── ROOM (día/tema)
              └── DRAWER (texto verbatim)
```
**Closets son conceptuales, no implementados como capa de storage separada** — el storage real sigue siendo drawer + metadata.

## 2. AAAK Dialect — resuelto con fuente primaria, sin ambigüedad
- Formato: `ZID:ENTITIES|topic_keywords|"key_quote"|WEIGHT|EMOTIONS|FLAGS`
- **ES CON PÉRDIDA, A PROPÓSITO Y ADMITIDO POR EL PROYECTO.** No contradice el principio "verbatim siempre" — es una capa de índice OPCIONAL y aparte, el storage default (ChromaDB, verbatim) nunca se toca.
- Benchmark oficial: modo verbatim crudo = 96.6% R@5. Modo AAAK = 84.2% R@5 — 12.4 puntos de regresión.
- Recomendación textual del propio proyecto: *"For most users, raw verbatim mode is the best default."* Usar `compress` solo con miles de sesiones/entidades muy repetidas, o modelos locales con contexto muy chico.

## 3. Nota para otras instancias de IA
- No activar `mempalace compress` en este palace salvo que el volumen de datos lo justifique de verdad (miles de sesiones). Confirmado con la fuente oficial, no es una precaución mía sin fundamento.
- Halls es la pieza de jerarquía que faltaba documentar — cuando decidamos wings para minar, pensar también en qué hall_* le corresponde a cada tipo de contenido.
