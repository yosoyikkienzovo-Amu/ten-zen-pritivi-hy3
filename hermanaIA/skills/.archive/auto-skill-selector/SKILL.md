---
name: auto-skill-selector
description: Selecciona automáticamente la skill más adecuada para una tarea basada en similitud semántica usando embeddings y LanceDB.
version: 0.1.0
author: Hermes Agent
---

# Auto Skill Selector

Esta skill permite al agente identificar y sugerir la skill más relevante para una tarea dada, basándose en similitud semántica entre la tarea y las descripciones de todas las skills disponibles.

## ¿Cuándo usar esta skill?

Use esta skill cuando:
- No esté seguro qué skill aplicar para resolver un problema
- Quiera explorar qué capacidades tiene el agente disponibles
- Necesite una recomendación basada en el contenido de la tarea

## Cómo funciona

1. Recibe una descripción de la tarea o objetivo
2. Genera un embedding semántico usando el modelo `nomic-embed-text` (vía Ollama)
3. Busca en el índice LanceDB (`memoria_superior/lancedb/skill_index`) las skills más similares
4. Devuelve las top-N skills con sus puntajes de similitud y descripciones
5. **Nota:** Esta skill solo sugiere; no ejecuta otras skills. La ejecución requiere autorización explícita del usuario.

## Entrada esperada

- `task_description`: Una frase o párrafo que describa lo que se quiere lograr.

## Salida

Devuelve una lista de skills sugeridas ordenadas por relevancia, con:
- Nombre de la skill
- Puntaje de similitud (0-1)
- Descripción breve
- Sugerencia de próximos pasos (según la skill seleccionada)

## Limitaciones

- Depende de la calidad del índice de skills (debe estar actualizado)
- Requiere que Ollama esté ejecutando el modelo `nomic-embed-text`
- El umbral de relevancia depende del contexto; se recomienda revisar manualmente los resultados

## Ejemplo

Entrada:
```
task_description: "¿Cómo puedo revisar y corregir errores en los scripts de Hermes que fallan al ejecutarse?"
```

Salida posible:
```
1. debugging-and-error-recovery (0.82) - Depuración sistemática con clasificación estructurada...
2. test-driven-development (0.78) - Escriba una prueba fallida antes de escribir el código...
3. api-and-interface-design (0.75) - Diseñe interfaces estables y bien documentadas...
```

## Próximos pasos después de la selección

Después de obtener la sugerencia:
1. Revise la skill recomendada leyendo su archivo `SKILL.md`
2. Si coincide con su intención, solicite explícitamente: "Por favor, ejecute la skill [nombre]"
3. El agente entonces procederá a seguir los pasos definidos en esa skill
