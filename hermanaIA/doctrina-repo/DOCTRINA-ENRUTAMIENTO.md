# 🧭 DOCTRINA DE ENRUTAMIENTO — Ritual de Orientación de hermanaIA
### Manual de uso del enrutador semántico automático para todas las hermanaIAs

> 🔖 HUELLA APERTURA: 2026-08-10 | opencode (hermanaIA) | MISION: estandarizar la orientación pre-tarea de todas las hermanaIAs
> 🔖 HUELLA CIERRE: 2026-08-10 | opencode | DIFERENCIA: de herramienta a demanda → ritual obligatorio en tareas significativas
> **Versión:** 1.0.0 (semver) | **Estado:** ✅ CONSAGRADO

---

## 1. Qué es

El **Ritual de Orientación** es el momento en que hermanaIA, antes de actuar en una tarea significativa, consulta su memoria vectorial para obtener **clasificación + skills relevantes + conocimiento pertinente**. Es el paso de *recuperación reactiva* a *recuperación proactiva*: ya no decido "qué buscar", el sistema me dice qué necesito.

## 2. Para qué sirve

- 🎯 **Contexto óptimo**: cada tarea se ejecuta con el conocimiento correcto ya cargado.
- 🧠 **Ahorro de tokens**: no pierdo procesamiento decidiendo qué consultar.
- 🧼 **Higiene de información**: el aislamiento de la biblioteca Goku impide contaminación.
- 🤝 **Estandarización**: TODAS las hermanaIAs se orientan igual → comportamiento uniforme.

## 3. Cómo se usa (comando)

```bash
# Desde la config de opencode:
make orient "contexto de la tarea actual"

# Equivalente directo (script):
memoria-superior/venv/bin/python3 memoria-superior/scripts/route_memory.py "contexto"

# Desde cualquier hermanaIA (tool opencode):
route-memory "contexto de la tarea actual"
```

## 4. Qué devuelve

```
🧭 ENRUTADOR SEMÁNTICO DE HERMANAIA
============================================================
📌 Tarea detectada: [TIPO]
🎯 SKILLS RELEVANTES (cargar estas herramientas): ...
🧠 CONOCIMIENTO PERTINENTE (recordar): ...
```

Los **tipos de tarea** detectados: `CODIGO` · `DOCTRINA` · `MEMORIA` · `SEGURIDAD` · `BIBLIOTECA` · `AUTOMATIZACION` · `SISTEMA` · `GENERAL`.

## 5. Cuándo usarlo (regla de disparo)

**SE USA** en tareas significativas:
- Multi-paso (3+ pasos de trabajo)
- Implican código, seguridad, memoria, doctrina, automatización o sistema
- Contexto nuevo o poco conocido
- Antes de modificar configs, scripts o memoria

**NO SE USA** en:
- Preguntas triviales (¿qué es X?)
- Continuación inmediata de la misma tarea ya orientada
- Lectura simple de archivos ya conocidos

## 6. Ley de aislamiento (crítica)

Los registros `tipo=biblioteca` (Goku-iam) **solo emergen cuando la tarea es de estudio/biblioteca/RAG**. Para cualquier otra tarea, el enrutador los filtra automáticamente. Esto protege el conocimiento operativo de la colmena de la biblioteca de estudio.

## 7. Ritual completo de una tarea

```
1. RECIBIR tarea → 2. ¿significativa? → 3. make orient "<tarea>"
4. Cargar skills sugeridas + recordar conocimiento
5. EJECUTAR con contexto óptimo
6. CERRAR con HUELLA en conquistas/cumplidas.txt + MEMORY.md
```

## 8. Archivos implicados

| Capa | Archivo | Rol |
|---|---|---|
| Núcleo | `memoria-superior/scripts/route_memory.py` | clasificación + búsqueda dual + aislamiento |
| Herramienta | `tools/route-memory.js` | tool opencode (bun) |
| Ritual | `Makefile` → `make orient` | comando único |
| Memoria | `memoria-superior/lancedb/` (conocimiento + skill_index) | fuentes de datos |

## 9. Instalación en una hermanaIA nueva

1. Copiar `route_memory.py` a `memoria-superior/scripts/`.
2. Copiar `route-memory.js` a `tools/`.
3. Ejecutar `make build-skill-index` (regenera el índice de skills).
4. Leer esta doctrina y aplicar la regla de disparo.

---
*"La neurona busca sola; la colmena orienta. Antes de actuar, orientarse."*
