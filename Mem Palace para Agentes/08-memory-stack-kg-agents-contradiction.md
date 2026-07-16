# MemPalace — Resumen 08: Memory Stack + Knowledge Graph + Specialist Agents + Contradiction Detection

Fuentes: mempalaceofficial.com/concepts/{memory-stack,knowledge-graph,agents,contradiction-detection}.html
Última verificación: 2026-07-15

## 1. Memory Stack (L0-L3) — completo
| Layer | Qué | Tamaño | Cuándo |
|---|---|---|---|
| L0 | Identidad | ~50-100 tokens | Siempre |
| L1 | Essential Story (top 15 momentos) | ~500-800 tokens | Siempre |
| L2 | Room Recall filtrado | ~200-500 c/u | Cuando el tema aparece |
| L3 | Deep Search semántico | Variable | Cuando se pide explícito |

Wake-up típico L0+L1: ~600-900 tokens (implementación actual; cifras de marketing de terceros dicen "170 tokens", no confirmado en la doc oficial — tratar 600-900 como la cifra confiable).

L1 se autogenera: lee todos los drawers, puntúa por importancia/peso emocional, toma el top 15, agrupa por room, trunca a 3200 caracteres.

Python: `from mempalace.layers import MemoryStack` → `.wake_up()`, `.recall(wing=)`, `.search(query)`, `.status()`

## 2. Knowledge Graph — completo
SQLite en `~/.mempalace/knowledge_graph.sqlite3`. Triples: subject → predicate → object, con `valid_from`/`valid_to` (NULL = vigente), `confidence` (0.0-1.0), `source_closet` (link al drawer verbatim).

```python
from mempalace.knowledge_graph import KnowledgeGraph
kg = KnowledgeGraph()
kg.add_triple("Kai", "works_on", "Orion", valid_from="2025-06-01")
kg.query_entity("Kai")                          # todo sobre Kai
kg.query_entity("Maya", as_of="2026-01-20")      # qué era cierto en esa fecha
kg.timeline("Orion")                             # historia cronológica
kg.invalidate("Kai", "works_on", "Orion", ended="2026-03-01")
```

## 3. Specialist Agents — CORRECCIÓN IMPORTANTE
**No existe registro de agentes.** La doc oficial dice literalmente: *"MemPalace does not currently ship an agent registry, ~/.mempalace/agents/*.json, or a mempalace_list_agents tool."* Ignorar cualquier fuente de terceros que hable de esto como funcional.

Lo que SÍ existe: diario simple por agente, vía MCP:
```
mempalace_diary_write { "agent_name": "reviewer", "entry": "PR#42|auth.bypass.found|..." }
mempalace_diary_read  { "agent_name": "reviewer", "last_n": 10 }
```
Cada agent_name mapea a su propio wing (`wing_reviewer`).

## 4. Contradiction Detection — NO IMPLEMENTADO
Confirmado con fuente oficial: *"Contradiction detection is a planned capability, not a shipped end-to-end feature... not a complete contradiction-checking tool exposed through the CLI or MCP server."* Los ejemplos de la doc son comportamiento intencionado, no lo que existe hoy. Las primitivas del knowledge graph (valid_from/valid_to) están, pero no hay checker automático.

## 5. Nota para otras instancias de IA
- No intentar configurar "agentes especializados descubribles" — usar el patrón simple de diary con agent_name fijo por rol si se quiere algo parecido.
- No depender de detección automática de contradicciones — si hace falta, hay que construirla a mano sobre las primitivas del KG (query_entity + invalidate manual).
