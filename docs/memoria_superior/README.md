# Memoria Superior para Agentes IA

## Overview
This module implements a hybrid memory system combining:
- **Vector Storage (LanceDB)**: For episodic memory with semantic search via embeddings.
- **Relational & Topological Memory (Obsidian Vault)**: Markdown notes with frontmatter for knowledge linking.
- **Contextual Reasoning (Ollama + LLM)**: Uses retrieved memories as context for a large language model to generate reasoned responses.

## Directory Structure
```
~/.hermes/memoria_superior/
├── lancedb/                # LanceDB vector storage
├── obsidian_vault/         # Obsidian markdown notes
├── scripts/                # Source code (memoria.py, tests, etc.)
├── n8n_workflows/          # Reserved for future n8n automation
└── docs/                   # Documentation (this file)
```

## Installation & Setup
1. **Ollama Models**: Ensure the following models are available:
   - `nomic-embed-text` (for embeddings, 768 dimensions)
   - A large reasoning model (e.g., `goku-llama3.1:latest` or `llama3.1:latest`)
   ```bash
   ollama pull nomic-embed-text
   ollama pull goku-llama3.1:latest
   ```
2. **Python Dependencies** (installed via `pip install --break-system-packages`):
   - `lancedb`
   - `pyarrow`
   - `requests`
   - `pyyaml`
   - `pandas` (optional, for some utilities)

## Usage
### Basic Initialization
```python
from memoria import MemoriaSuperior

memoria = MemoriaSuperior(
    lancedb_path="~/.hermes/memoria_superior/lancedb",
    obsidian_vault="~/.hermes/memoria_superior/obsidian_vault",
    ollama_host="http://localhost:11434",
    embed_model="nomic-embed-text",
    reasoning_model="goku-llama3.1:latest"
)
```

### Adding a Memory
```python
result = memoria.add_memory(
    text="Hoy aprendí sobre la integración de LanceDB y Obsidian para la memoria superior de agentes.",
    room_id="vestibulo_contexto",
    metadata={"title": "Aprendizaje del día", "tags": ["aprendizaje", "integración"]},
    tags=["aprendizaje", "integración", "memoria"]
)
# Returns dict with id, episodio, obsidian_link, room_id, timestamp, embedding_dim
```

### Searching Memories
```python
results = memoria.search_memories(
    text="¿Qué aprendí sobre LanceDB?",
    limit=5
)
```

### Retrieving Recent Memories
```python
recent = memoria.get_recent_memories(limit=10)
```

### Retrieving by ID
```python
mem = memoria.get_memory_by_id(some_uuid)
```

### Contextual Reasoning
```python
reasoning = memoria.reason_with_context(
    query="¿Qué he aprendido recientemente sobre memoria y conocimiento?",
    context_limit=5,
    temperature=0.7,
    max_tokens=500
)
```
**Note**: The first call to a large model may experience latency as Ollama loads the model into VRAM/RAM. Subsequent calls are faster.

## Design Notes
- **Embedding Model**: `nomic-embed-text` is used for all vector operations, ensuring semantic search quality.
- **Reasoning Model**: By default `goku-llama3.1:latest` (or any large model set via `MEMORY_REASONING_MODEL` env var). The system is designed to work with any Ollama-compatible LLM.
- **Obsidian Integration**: Each memory creates a note in the vault with frontmatter containing:
  - `id`: UUID of the memory
  - `tipo`: `"episodio_agente"`
  - `palacio_room`: The `room_id` (e.g., `vestibulo_contexto`)
  - `tags`: User-defined tags plus defaults
  - `referencias_vectores`: Self-reference (can be extended for cross-references)
  - `timestamp`: ISO timestamp
- **Error Handling**: The module raises exceptions for embedding/reasoning failures and returns error strings for reasoning timeouts (configurable timeout).

## Performance & Known Considerations
- **First‑Reasoning Latency**: The initial call to a large LLM (e.g., `goku-llama3.1:latest`) may take 20‑60 seconds as Ollama loads the model. This is expected behavior, not a bug.
- **Timeouts**: Reasoning calls use a 120‑second timeout to accommodate model loading and generation. Adjust via code if needed.
- **Scalability**: LanceDB scales to millions of vectors; the Obsidian vault scales with the number of notes (filesystem limits apply).

## Extending the System
- **Custom Metadata**: Pass additional fields in `metadata`; they will be stored in the LanceDB record and added to the Obsidian note’s frontmatter.
- **Alternative Models**: Change `embed_model` and `reasoning_model` via constructor arguments or environment variables.
- **Integration Hooks**: The `n8n_workflows/` directory is ready for future automation (e.g., syncing with external triggers).

## License
Internal use under the Hermes Agent framework.

--- 
*Last updated: 2026-07-17*