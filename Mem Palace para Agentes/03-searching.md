# MemPalace — Resumen 03: Searching Memories

Fuente: https://mempalaceofficial.com/guide/searching.html
Última verificación: 2026-07-13

## 1. Base
Búsqueda semántica vectorial vía ChromaDB. Resultados **verbatim** — nunca resúmenes del motor.

## 2. CLI Search
```
mempalace search "why did we switch to GraphQL"
mempalace search "database decision" --wing myapp
mempalace search "auth decisions" --room auth-migration
mempalace search "pricing" --wing driftwood --room costs
mempalace search "deploy process" --results 10
```

## 3. Cómo funciona
1. Query embebida con `all-MiniLM-L6-v2` (backend ChromaDB default).
2. Comparación por similitud coseno contra todos los drawers.
3. Filtros wing/room acotan el scope (filtrado de metadata del vector store).
4. Devuelve resultados con score + metadata de origen.

### Por qué importa el scoping (clave para tokens)
Sin wing/room, cada búsqueda escanea TODO el palace y trae ruido de proyectos no relacionados. El filtrado es la herramienta principal para mantener retrieval predecible y barato en tokens a medida que el palace crece.

## 4. Búsqueda programática (Python)
```python
from mempalace.searcher import search_memories
results = search_memories(query="auth decisions", palace_path="~/.mempalace/palace",
                           wing="myapp", room="auth", n_results=5)
for hit in results["results"]:
    print(f"[{hit['similarity']}] {hit['wing']}/{hit['room']}")
```
Retorna dict con `query`, `filters`, `results` (cada uno con `text`, `wing`, `room`, `source_file`, `similarity`).

## 5. MCP Search
Conectado vía MCP, la IA busca sola llamando `mempalace_search` — el usuario nunca escribe comandos.

## 6. Wake-Up Context — respuesta directa al problema de tokens
```
mempalace wake-up
mempalace wake-up --wing driftwood
```
Carga **Layer 0** (identidad, siempre) + **Layer 1** (historia esencial) como contexto acotado de arranque (~600-900 tokens típico), ANTES de la primera llamada de retrieval. Arquitectura de 4 capas L0–L3 (ver Memory Stack, pendiente).

## 7. Nota para otras instancias de IA — Estrategia de tokens
1. **Nunca cargar el palace completo en contexto.** Solo se recupera lo que pide `search` (acotado con `--results N`) o el paquete compacto de `wake-up`.
2. **Wing/room scoping = primera línea de defensa contra ruido de tokens.**
3. Flujo por sesión: `wake-up [--wing X]` al arrancar → `search` puntual con filtros durante la conversación, nunca sin filtros en un palace multi-proyecto.
4. Pendiente confirmar: `mempalace compress` (visto en `--help`, "~30x reduction") — candidato clave para la estrategia de tokens a largo plazo. Ver Reference/CLI o Configuration.
