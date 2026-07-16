# 01 — Arquitectura: Alas, Salas, Cajones, Túneles y AAAK

Fuente: material técnico provisto por el usuario (mismo origen que 00).
Registrado: 2026-07-13

## 1. Flujo general
```
User → CLI / MCP Server → Storage Backend (ChromaDB por defecto, intercambiable)
                        → SQLite (knowledge graph)
```

## 2. Estructura del Palace
```
WING (persona/proyecto)
  └── ROOM (día/tema)
        └── DRAWER (fragmento de texto verbatim)
```
- **WING** = ala. Categoría amplia: una persona o un proyecto.
- **ROOM** = sala. Agrupación temporal/temática dentro del ala: un día o una sesión.
- **DRAWER** = cajón. La unidad atómica: un fragmento de texto exacto, sin alterar.

## 3. Capa de índice — AAAK
```
Índice AAAK:
  Punteros comprimidos → ubicaciones de DRAWER
  Escaneados por el LLM para encontrar drawers relevantes sin leer todo el contenido
```
Formato simbólico compacto (`dialect.py`). Permite que un LLM escanee miles de entradas de índice **instantáneamente** y sepa qué cajón abrir, sin cargar el contenido completo de cada uno. Es la pieza que hace viable escalar el palace sin quemar tokens.

## 4. Knowledge Graph (SQLite, separado del vector store)
```
ENTIDAD → PREDICADO → ENTIDAD   (con fechas valid_from / valid_to)
```
Grafo de relaciones entidad-entidad con vigencia temporal. Esto es distinto de la búsqueda semántica vectorial (ChromaDB): el KG guarda **hechos estructurados** (ej. "Fulano trabaja en X desde fecha Y"), no fragmentos de texto libre. Se consulta con las tools `mempalace_kg_*` (ver resumen 04-mcp-integration.md).

## 5. Túneles (Tunnels)
Puentes explícitos entre wings distintos, para cuando un tema conecta a dos proyectos/personas separadas. Se gestionan con `mempalace_create_tunnel`, `mempalace_list_tunnels`, `mempalace_follow_tunnels` (MCP) — ver resumen 04.

## 6. Nota para otras instancias de IA
- **Regla mental simple:** Wing = quién/qué proyecto. Room = cuándo/qué tema dentro de ese wing. Drawer = el texto exacto. AAAK = el índice que te deja encontrar el drawer correcto sin leer todo.
- Cuando decidamos la estrategia de minado (pendiente, según lo acordado con el usuario), la pregunta clave por cada fuente de datos es: **¿qué wing le corresponde?** Un wing mal definido =  búsquedas ruidosas después (ver resumen 03, sección "por qué importa el scoping").
- El Knowledge Graph es una estructura PARALELA al vector search, no un reemplazo. Para "qué dijo X sobre Y" → vector search (`mempalace_search`). Para "¿desde cuándo trabaja X en Y?" o relaciones con vigencia temporal → Knowledge Graph (`mempalace_kg_query`, `mempalace_kg_timeline`).
- Túneles son manuales/explícitos — no se crean solos. Si dos wings comparten contexto real (ej. un proyecto y la persona que lo lidera), vale la pena crear el túnel a propósito en vez de depender solo de cross-project search.
