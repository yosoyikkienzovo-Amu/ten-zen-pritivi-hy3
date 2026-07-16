# 02 — Estructura del Proyecto (código fuente)

Fuente: material técnico provisto por el usuario (mismo origen que 00).
Registrado: 2026-07-13

## 1. Árbol de módulos (`mempalace/`)
| Archivo | Rol |
|---|---|
| `mcp_server.py` | Servidor MCP — todas las tools de lectura/escritura |
| `cli.py` | Dispatcher de la CLI |
| `config.py` | Configuración + validación de input |
| `miner.py` | Minero de archivos de proyecto |
| `convo_miner.py` | Minero de transcripciones de conversación |
| `searcher.py` | Búsqueda semántica (híbrida BM25 + vector) |
| `knowledge_graph.py` | Grafo temporal entidad-relación (SQLite) |
| `palace.py` | Operaciones compartidas del palace |
| `palace_graph.py` | Recorrido de rooms + túneles cross-wing |
| `backends/base.py` | Interfaz abstracta — implementar para nuevos backends |
| `backends/chroma.py` | Implementación ChromaDB (default) |
| `dialect.py` | Dialecto de compresión AAAK |
| `normalize.py` | Detección y normalización de formato de transcripción |
| `entity_detector.py` | Auto-detección de personas/proyectos desde contenido |
| `entity_registry.py` | Almacenamiento y desambiguación de entidades |
| `layers.py` | Stack de wake-up de memoria L0–L3 |
| `onboarding.py` | Setup interactivo de primer uso |
| `repair.py` | Reparación y chequeos de consistencia del palace |
| `dedup.py` | Deduplicación |
| `migrate.py` | Migración de versión de ChromaDB |
| `spellcheck.py` | Auto-corrección de mensajes del usuario |
| `exporter.py` | Exportación de datos del palace |
| `hooks_cli.py` | CLI de gestión de hooks |
| `query_sanitizer.py` | Prevención de contaminación de prompts |
| `split_mega_files.py` | Split de archivos de transcripción concatenados |
| `version.py` | Fuente única de verdad de la versión |

## 2. Hooks (`hooks/`)
| Archivo | Rol |
|---|---|
| `mempal_save_hook.sh` | Hook `Stop` — dispara guardado de diary |
| `mempal_precompact_hook.sh` | Hook `PreCompact` — guarda estado antes de compresión |

## 3. Archivos clave por tarea común
| Tarea | Archivo(s) |
|---|---|
| Agregar una tool MCP | `mempalace/mcp_server.py` — agregar función handler + entrada en el diccionario TOOLS |
| Cambiar comportamiento de búsqueda | `mempalace/searcher.py` |
| Modificar minería de proyecto | `mempalace/miner.py` |
| Modificar minería de transcripciones | `mempalace/convo_miner.py` |
| Agregar un backend de almacenamiento | Subclase de `mempalace/backends/base.py`, registrar en `backends/__init__.py` |
| Validación de input | `mempalace/config.py` → `sanitize_name()` / `sanitize_content()` |
| Tests | Estructura espejo en `tests/test_<module>.py` |

## 4. Nota para otras instancias de IA
- **Dato nuevo no visto en la doc web hasta ahora:** `searcher.py` implementa búsqueda **híbrida BM25 + vector**, no solo vector cosine puro como sugería la página "Searching Memories" (resumen 03). BM25 es keyword/lexical matching; combinado con embeddings semánticos da mejor recall en términos exactos (nombres propios, IDs, código) que vector puro. Pendiente de confirmar si esto es configurable o siempre-on — candidato a revisar en Configuration o Reference/CLI.
- Si en algún momento se quiere extender MemPalace (nueva tool, nuevo backend), esta tabla de "archivo por tarea" es el mapa directo — no hace falta explorar todo el repo.
- `query_sanitizer.py` existe específicamente para prevenir contaminación de prompts — relevante si se mina contenido no confiable (ej. transcripts con texto pegado de terceros).
