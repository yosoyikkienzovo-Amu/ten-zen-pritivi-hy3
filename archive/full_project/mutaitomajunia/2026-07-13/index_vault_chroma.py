"""
Second-brain indexer for Obsidian vault.

Pipeline:
  Obsidian (.md) -> chunk -> Ollama embedding -> ChromaDB (vector store)
Optionally mirrored to LanceDB / Qdrant for heavier vaults.

Hardware target: Dell Latitude E5440, 16 GB RAM, Pop!_OS 24.04
  - Embeddings + LLM run locally via Ollama (CPU, layers offloaded to iGPU via Vulkan when available).
  - ChromaDB embedded (DuckDB/SQLite) keeps RAM footprint low.

Install:
  pip install chromadb ollama
  ollama pull nomic-embed-text      # small, fast local embedding model
  ollama pull qwen2.5:7b-q4_K_M     # reasoning model (quantized)

Run:
  python index_vault.py
"""

from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions
import ollama

# --- Config -------------------------------------------------------------
VAULT_PATH = Path("/home/ikki/ObsidianVault")   # <-- your vault
COLLECTION = "obsidian_vault"
EMBED_MODEL = "nomic-embed-text"                # local embedding model
CHUNK_CHARS = 1500                              # chunk size for big notes
CHUNK_OVERLAP = 200
# ------------------------------------------------------------------------

client = chromadb.PersistentClient(path=str(VAULT_PATH / ".chroma"))
ef = embedding_functions.OllamaEmbeddingFunction(model_name=EMBED_MODEL)
collection = client.get_or_create_collection(
    name=COLLECTION,
    embedding_function=ef,
    metadata={"hnsw:space": "cosine"},
)


def chunk_text(text: str) -> list[str]:
    if len(text) <= CHUNK_CHARS:
        return [text]
    chunks, start = [], 0
    while start < len(text):
        end = min(start + CHUNK_CHARS, len(text))
        chunks.append(text[start:end])
        start += CHUNK_CHARS - CHUNK_OVERLAP
    return chunks


def index_vault() -> None:
    ids, docs, metas = [], [], []
    for md in VAULT_PATH.rglob("*.md"):
        content = md.read_text(encoding="utf-8", errors="ignore")
        for i, chunk in enumerate(chunk_text(content)):
            ids.append(f"{md.stem}:{i}")
            docs.append(chunk)
            metas.append({"path": str(md), "name": md.name, "chunk": i})
    if not docs:
        print("No markdown notes found in vault.")
        return
    # Upsert; ChromaDB dedupes by id, so re-runs are safe.
    collection.upsert(documents=docs, ids=ids, metadas=metas)
    print(f"Indexed {len(docs)} chunks from {len(ids)} notes.")


def query(question: str, n: int = 5) -> None:
    res = collection.query(query_texts=[question], n_results=n)
    for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
        print(f"\n--- {meta['path']} (chunk {meta['chunk']}) ---\n{doc[:400]}...")


if __name__ == "__main__":
    index_vault()
    # Local LLM answer (layer-offloaded CPU inference via Ollama)
    q = input("\nPregunta (vacío para salir): ").strip()
    while q:
        query(q)
        q = input("\nPregunta (vacío para salir): ").strip()
