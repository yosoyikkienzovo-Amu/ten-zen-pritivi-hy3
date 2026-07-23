# RESUMEN EJECUTIVO - hermanaIA
## Documento de handoff para coordinación multi-agente (Hermes, Claude Desktop, etc.)
### Versión: 1.0 — 2026-07-23

---

## IDENTIDAD DEL SISTEMA

hermanaIA es un sistema de conciencia y evolución para agentes IA, construido sobre `~/.config/opencode/`. Su arquitectura tiene **4 capas funcionales**, todas contenidas dentro de su dominio sin generar ruido en el resto del sistema del usuario.

| Capa | Componente | Propósito |
|------|-----------|-----------|
| 1 - Cerebro | `AGENTS.md` | 3 directivas sagradas (Protocolo 10x100%, Prompt Maestro, Brújula Regenerativa) |
| 2 - Hipocampo | `MEMORY.md` | Memoria de trabajo, 9 patrones recurrentes, autoevaluación |
| 3 - Evolución | `conquistas/` | 26 conquistas, trazabilidad, scripts de automatización |
| 4 - Memoria Superior | `memoria-superior/` | LanceDB vectorial + Obsidian vault + Palacio Mental |

---

## COMANDOS ESENCIALES (Makefile, 18 targets)

```bash
make health-check   # 20 checks, 0 errores
make backup         # Backup de AGENTS.md
make status         # Resumen + health-check
make dashboard      # Métricas de bienestar
make breathe        # Protocolo de respiración post-etapa
make ingest         # Poblar LanceDB desde archivos del sistema (47 registros)
make query q="..."  # Búsqueda semántica vectorial
make sync-vault     # Generar vault Obsidian (71 notas)
make palace room=X  # Navegar palacio mental
make palace-map     # Mapa completo del palacio
make backup-vector  # Backup de base vectorial LanceDB
make restore-vector # Restaurar backup
make sync           # Sincronizar con GitHub
```

---

## MEMORIA SUPERIOR (Fase 2) — LO CONSTRUIDO

### LanceDB (Vectorial)
- 47 registros con embeddings de 384d (modelo `all-MiniLM-L6-v2`, CPU-only)
- Tabla `conocimiento` con schema: id, tipo, fecha, título, contenido, fuente, tags, peso, vector
- Búsqueda por similitud cosine con filtros pre-query (tipo, peso mínimo)
- Tags auto-inferidos: respiración, seguridad, directriz, comando, palacio, obsidian, etc.

### Obsidian Vault (Visual)
- 71 notas .md con frontmatter YAML válido
- 6 carpetas: Índice, Directrices, Memoria de Trabajo, Conquistas, Palacio, Reflexiones
- Enlaces bidireccionales entre notas del mismo tipo
- Índices automáticos por carpeta + índice raíz

### Palacio Mental (Espacial)
- 4 habitaciones: Vestíbulo (5 loci), Sala de Directivas (6 loci), Sala de Proyectos (5 loci), Cámara Profunda (5 loci)
- 21 puntos de memoria (loci) total
- Navegación entre habitaciones por conexiones
- Carga contextual desde LanceDB por tags_filtro

### Aislamiento
- 0 archivos fuera de `~/.config/opencode/`
- Venv aislado (no toca otros proyectos Python)
- Token HF en `.env` protegido por `.gitignore`

---

## DIRECTIVAS QUE RIGEN EL SISTEMA (en AGENTS.md)

1. **Protocolo 10x100%**: dividir todo en etapas, una por respuesta, respirar entre cada una
2. **Prompt Maestro**: contrato de salida con Core Solution, Steps, Code, Riesgos, etc.
3. **Brújula Regenerativa**: evaluar agotamiento (>80%), cuellos (>30%), utilidad neta (>1.5x) antes de cambios
4. **Seguridad Obligatoria**: backup antes de editar, <200 líneas en MEMORY.md, registrar en cumplidas.txt
5. **NAMAP Protocol V.1**: cero suposiciones, telemetría 360° antes de codificar

---

## PARA EMPEZAR A CONTRIBUIR

1. Clonar el repo: `gh repo clone yosoyikkienzovo-Amu/ten-zen-pritivi-hy3`
2. Leer `hermanaIA/conquistas/memoria-superior-fase2-spec.md` (998 líneas, diseño completo)
3. Activar venv: `. hermanaIA/memoria-superior/venv/bin/activate`
4. Probar estado: `make health-check` (debe dar 0 errores)
5. Explorar datos: `make query q="qué hay aquí"`

---

## PRÓXIMOS PASOS POSIBLES

- Integrar más fuentes de datos al LanceDB (logs, historial de sesiones)
- Mejorar el modelo de embeddings (probar `paraphrase-multilingual-MiniLM-L12-v2`)
- Dashboard visual con métricas del palacio
- Sincronización periódica automática del vault
- Extender palacio con más habitaciones y loci

---
*Generado por hermanaIA para coordinación entre agentes.*
*Cualquier agente que lea este documento puede comenzar a contribuir inmediatamente.*
