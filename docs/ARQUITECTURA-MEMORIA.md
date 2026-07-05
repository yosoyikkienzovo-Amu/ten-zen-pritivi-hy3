# 📐 Plano: Arquitectura de Memoria de TEN-ZEN (v2.0)

## ⚖️ Principio Rector: Soberanía Dual
Todo servicio ejecutable tiene un gemelo: una ruta **Online** (Potencia) y una **Offline** (Soberanía), ambas Open Source. El sistema debe ser capaz de conmutar automáticamente (failover).

| Capa | Online (Nube) | Offline (Local) | Función |
| :--- | :--- | :--- | :--- |
| **LLM** | OpenRouter | Ollama | Razonamiento |
| **Embeddings** | Voyage / OpenAI | Ollama (bge-m3) | Vectorización |
| **Recall** | Qdrant Cloud | Chroma / Qdrant Local | Memoria Semántica |
| **Grafo** | Neo4j Aura | FalkorDB | Memoria Temporal |
| **Automatización** | n8n Cloud | n8n Self-hosted | Dream Pass |

## 🌀 El "Dream Pass" (Aprendizaje Ascendente)
Es el proceso nocturno automatizado que garantiza el minimalismo y la evolución:
1. **Relectura:** El sistema analiza los nuevos datos del día.
2. **Elevación:** Las correcciones repetidas se suben a "Preferencias Confirmadas".
3. **Poda:** Se elimina lo obsoleto y se invalidan las contradicciones.
4. **Mutación:** Se actualizan los hexagramas del I-Ching según el nuevo estado.

## 🏛️ Seguridad y Acceso
- **Tailscale/WireGuard:** Sustituye a ngrok. Cero puertos abiertos al público.
- **MCP Server:** Toda la memoria se expone vía Model Context Protocol para que cualquier agente (TEN-ZEN, Kumi, Claude) lea la misma fuente de verdad.

---
*Diseñado para la autonomía impecable y el ahorro de tiempo del humano.*
