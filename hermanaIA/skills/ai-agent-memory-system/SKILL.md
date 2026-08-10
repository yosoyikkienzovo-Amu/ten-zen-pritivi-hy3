---
name: ai-agent-memory-system
description: Set up and use advanced memory systems for AI agents combining vector databases (LanceDB), contextual note-taking (Obsidian), and local embeddings (Ollama).
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [memory, agent, llm, embeddings, vectordb, obsidian]
    related_skills: [hermes-agent, nota-taking, mlops]
---

# AI Agent Memory System

## Overview

This skill covers setting up a sophisticated memory system for AI agents that combines:
- **LanceDB**: Vector storage for semantic search and embeddings
- **Obsidian**: Markdown-based knowledge base for contextual, linked notes  
- **Ollama**: Local LLM for generating embeddings (using models like nomic-embed-text)

This creates a "Memoria Superior" system that enables agents to store, retrieve, and relate experiences with semantic understanding.

## When to Use

- Building AI agents that need long-term memory
- Creating personal knowledge assistants
- Developing systems that learn from past interactions
- Implementing Retrieval-Augmented Generation (RAG) for local LLMs
- When you need persistent, searchable conversation history

## System Components

### 1. Vector Database (LanceDB)
- Stores embeddings of experiences/thoughts
- Enables semantic similarity search
- Schema: vector (768-dim), id, episode, obsidian_link, room_id, timestamp

### 2. Contextual Knowledge Base (Obsidian)
- Markdown files with YAML frontmatter
- Bidirectional linking between notes
- Tags and metadata for organization
- Human-readable and editable

### 3. Embedding Generator (Ollama)
- Local model for creating text embeddings
- Uses nomic-embed-text (768 dimensions) by default
- No API calls needed - runs locally

## Installation & Setup

### Prerequisites

1. **Ollama** installed and running
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Start the service
   ollama serve
   
   # Pull the embedding model
   ollama pull nomic-embed-text
   ```

2. **Python packages**
   ```bash
   pip install lancedb pyarrow requests pyyaml --break-system-packages
   ```

3. **Directory Structure**
   The system expects:
   ```
   ~/.hermes/memoria_superior/
   ├── lancedb/           # LanceDB database
   └── obsidian_vault/    # Obsidian markdown notes
   ```

### Configuration

The `MemoriaSuperior` class in `~/.hermes/scripts/memoria_superior/memoria.py` can be customized via:

- Environment variables:
  - `MEMoir_LANCEDB_PATH` (default: `~/.hermes/memoria_superior/lancedb`)
  - `MEMoir_OBSIDIAN_VAULT` (default: `~/.hermes/memoria_superior/obsidian_vault`)
  - `OLLAMA_HOST` (default: `http://localhost:11434`)
  - `MEMORY_EMBED_MODEL` (default: `nomic-embed-text`)

## Core Functions

### `MemoriaSuperior.add_memory()`
Add a new episodic memory:

```python
result = memoria.add_memory(
    episode_text="Your experience or thought here",
    room_id="vestibulo_contexto",  # Memory palace room
    metadata={"title": "Memory Title", "tags": ["tag1", "tag2"]},
    tags=["additional", "contextual", "tags"]
)
```

Returns:
```json
{
  "id": "uuid",
  "episodio": "The stored text",
  "obsidian_link": "relative/path/to/note.md",
  "room_id": "vestibulo_contexto",
  "timestamp": "ISO timestamp",
  "embedding_dim": 768
}
```

### `MemoriaSuperior.search_memories()`
Semantic search for related memories:

```python
results = memoria.search_memories(
    query_text="What did I learn about X?",
    room_id="optional_room_filter",
    limit=5
)
```

### `MemoriaSuperior.get_recent_memories()`
Get most recent memories by timestamp.

## Verification

Run the built-in verification script:

```bash
python ~/.hermes/scripts/memoria_superior/verify_setup.py
```

This checks:
1. Ollama availability and nomic-embed-text model
2. LanceDB database and schema
3. Obsidian vault and sample note

## Usage Example

```python
from memoria import MemoriaSuperior

# Initialize (uses default paths)
memoria = MemoriaSuperior()

# Add a memory from a conversation
conversation_summary = "User asked about setting up memory systems. We discussed LanceDB, Obsidian, and Ollama integration."
memory = memoria.add_memory(
    episode_text=conversation_summary,
    room_id="conversaciones",
    metadata={
        "title": "Memory System Discussion",
        "tags": ["memory", "setup", "discussion"]
    },
    tags=["conversation", "technical", "setup"]
)

print(f"Stored memory ID: {memory['id']}")
print(f"Associated note: {memory['obsidian_link']}")

# Later, search for related memories
related = memoria.search_memories(
    query_text="How to set up vector databases?",
    limit=3
)
```

## Customization

### Memory Palace Rooms
Organize memories by context:
- `vestibulo_contexto` - General conversations
- `sala_estudio` - Learning and research
- `laboratorio` - Experiments and coding
- `galeria` - Creative ideas
- `biblioteca` - Reference knowledge

### Obsidian Note Format
Each memory creates a note with frontmatter:

```markdown
---
id: "uuid"
tipo: "episodio_agente"
palacio_room: "vestibulo_contexto"
tags:
  - memoria
  - episodio_agente
  - [custom tags]
referencias_vectores: ["uuid"]  # Self-reference, can be expanded
timestamp: "ISO timestamp"
---

[The actual memory content]
```

## Integration with Hermes

This memory system can be used:
1. **Directly in Python scripts** as shown above
2. **Through custom Hermes tools** wrapped in skills
3. **In agent loops** to automatically store and recall experiences
4. **For persistent context** across sessions

## Maintenance

### Backing Up
Both components are file-based:

```bash
# Backup LanceDB (copy the directory)
cp -r ~/.hermes/memoria_superior/lancedb ~/backups/

# Backup Obsidian vault
cp -r ~/.hermes/memoria_superior/obsidian_vault ~/backups/
```

### Migration
To move the system to a new location:
1. Copy both directories
2. Update environment variables or reconfigure paths
3. The system will automatically use the new locations

## Troubleshooting

### "Field 'episodio' does not exist in table schema"
This means the LanceDB table schema doesn't match expectations. Fix by:
1. Ensuring the table was created with the correct schema (check that field names match exactly, including language - e.g., "episodio" not "episode")
2. Verifying that your code uses the same field names as the schema (look for inconsistencies like "episode" vs "episodio")
3. If needed, delete and recreate the table (this will lose stored memories)

Specific fix from session: Ensure all references to the episode field use "episodio" (Spanish) to match the HTML schema reference, not "episode" (English).

### Ollama Connection Issues
- Verify `ollama serve` is running
- Check that `nomic-embed-text` is pulled: `ollama list`
- Ensure `OLLAMA_HOST` environment variable is correct

### Permission Errors
- Ensure the `~/.hermes/memoria_superior/` directory is writable
- The system automatically creates directories if missing

## Performance Notes
- Embedding generation is the slowest part (depends on your hardware and model)
- LanceDB queries are typically very fast (<10ms for small-medium datasets)
- Obsidian file creation is nearly instantaneous
- Consider batching multiple memory additions if latency is critical
## Extensions

### Advanced Features to Consider

1. **Memory Consolidation**
   - Periodically summarize and compress old memories
   - Create "memory threads" that connect related episodes

2. **Relationship Mapping**
   - Expand `referencias_vectores` to link to related memories
   - Implement spreading activation for memory retrieval

3. **Multi-Modal Memories**
   - Extend to store image/audio embeddings
   - Use multi-modal models from Ollama library

4. **Integration with Agent Frameworks**
   - Hook into agent observation/action cycles
   - Automatically store perceptions and decisions

5. **Contextual Reasoning**
   - Retrieve relevant memories using semantic search
   - Use large language models (like goku-llama3.1:latest) to reason over memories
   - Generate insights and answers based on stored experiences

## Related Systems

This implementation draws inspiration from:
- MemGPT and hierarchical memory systems
- Zettelkasten method via Obsidian
- Vector databases for semantic search
- Local LLM privacy-first approaches

## Verification Checklist

- [ ] Ollama is running and `nomic-embed-text` model is available
- [ ] Python packages `lancedb`, `pyarrow`, `requests`, `pyyaml` installed
- [ ] Directories `~/.hermes/memoria_superior/lancedb` and `~/.hermes/memoria_superior/obsidian_vault` exist
- [ ] LanceDB table `memoria_superior` has correct schema
- [ ] Can add a memory and generate an embedding
- [ ] Created memory produces corresponding Obsidian note
- [ ] Search functionality returns relevant results
- [ ] Recent memories are retrievable in chronological order

## Example Automation

Create a cron job to periodically reflect on recent memories:

```bash
# Daily reflection at 8 PM
0 20 * * * ~/.hermes/scripts/memoria_superior/reflect_on_memories.py
```

Where `reflect_on_memories.py` might:
1. Retrieve today's memories
2. Ask an LLM to summarize insights
3. Store the reflection as a new meta-memory

## References

- LanceDB documentation: https://lancedb.github.io/
- Obsidian Help: https://help.obsidian.md/
- Ollama: https://ollama.com/
- Nomix Embed Text: https://huggingface.co/nomic-ai/nomic-embed-text-v1.5

## See Also

- `hermes-agent` skill for general Hermes configuration
- `nota-taking` skill for Obsidian-specific workflows
- `mlops` skill for machine learning operations patterns

---
*This system enables AI agents to develop persistent, semantic memory inspired by cognitive science principles while maintaining privacy through local processing.*