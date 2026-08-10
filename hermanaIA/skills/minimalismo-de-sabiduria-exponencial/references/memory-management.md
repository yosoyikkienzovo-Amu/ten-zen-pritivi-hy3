# Gestión de Memoria Hermes - TEN-ZEN PRITivi HY3

## Problema: Memoria Llena (2,200 caracteres)
Si al intentar `memory action=add` se recibe el error:
`"Adding this entry (X chars) would exceed the limit. Replace or remove existing entries first."`

## Solución: Reemplazo (Patch)
No intentar añadir más. Se debe reemplazar una entrada antigua o menos vital.

### Pasos:
1. Identificar entrada a reemplazar (ej: "Estructura de carpetas completa" si ya no es crítica).
2. Usar `memory action=replace` con `old_text` exacto y `new_text` conteniendo la nueva información.
3. Mantener declaraciones de hechos (formato: "Usuario prefiere X", no "Hacer X").

## Ejemplo de Reemplazo Exitoso
```json
{
  "action": "replace",
  "target": "memory",
  "old_text": "\"Estructura de carpetas completa\" - Ruta base: ...",
  "new_text": "\"Nuevas Habilidades Adquiridas\" - Integración de awesome-openclaw..."
}
```

## Regla de Oro
- Mantener memoria enfocada en hechos que importarán más tarde.
- Evitar guardar progreso de tareas, resultados de sesión o estado temporal.
- Si se descubre un nuevo flujo de trabajo, guardarlo como SKILL, no en memoria.
