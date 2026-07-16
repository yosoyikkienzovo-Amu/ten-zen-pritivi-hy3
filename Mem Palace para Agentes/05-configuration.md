# MemPalace — Resumen 05: Configuration

Fuente: https://mempalaceofficial.com/guide/configuration.html
Última verificación: 2026-07-15

## 1. Config global — `~/.mempalace/config.json`
```json
{
  "palace_path": "/custom/path/to/palace",
  "collection_name": "mempalace_drawers",
  "people_map": {"Kai": "KAI", "Priya": "PRI"},
  "max_backups": 10
}
```
| Key | Default | Descripción |
|---|---|---|
| `palace_path` | `~/.mempalace/palace` | Dónde vive el palace local por defecto |
| `collection_name` | `mempalace_drawers` | Nombre de colección del backend default |
| `people_map` | `{}` | Mapeo nombre de entidad → código AAAK |
| `max_backups` | `10` | Backups timestamped a conservar. `0` = conservar todos |

## 2. Backends de storage — todos opt-in salvo ChromaDB
| Backend | Modo | Instalación | Namespaces | Lexical | Config |
|---|---|---|---|---|---|
| `chroma` (default) | Local embebido | incluido | – | ✓ | – |
| `sqlite_exact` | Local exacto | incluido | – | ✓ | – |
| `milvus` | Local Lite / Server opt-in | `mempalace[milvus]` | ✓ | ✓ | `MEMPALACE_MILVUS_URI` |
| `qdrant` | Server REST | incluido | ✓ | ✓ | `MEMPALACE_QDRANT_URL` |
| `pgvector` | Server Postgres | `mempalace[pgvector]` | ✓ | ✓ | `MEMPALACE_PGVECTOR_DSN` |

Selección: `--backend <name>`, `MEMPALACE_BACKEND=<name>`, o `"backend"` en config.json. Advertencia oficial: si un backend server-mode apunta a algo que no es tu propio servicio, MemPalace manda y guarda texto verbatim + metadata ahí — decisión explícita, nunca default.

## 3. Variables por backend
- Milvus: `MEMPALACE_MILVUS_URI`, `_TOKEN`, `_DB_NAME`, `_NAMESPACE`, `_CONSISTENCY_LEVEL` (default `Strong`)
- Qdrant: `MEMPALACE_QDRANT_URL` (default `http://localhost:6333`), `_API_KEY`, `_NAMESPACE`, `_TIMEOUT` (default `10.0`)
- Pgvector: `MEMPALACE_PGVECTOR_DSN` (default `postgresql://localhost:5432/mempalace`), `_NAMESPACE`

## 4. Config de proyecto (generada por `mempalace init`)
- `mempalace.yaml` → `wing`, `rooms: [...]`, `palace_path`
- `entities.json` → mapeo nombre→código AAAK

## 5. Identity file
`~/.mempalace/identity.txt` — texto plano, es la Layer 0 (siempre cargada). Primera persona, self-concept de la IA al despertar.

## 6. Otros
- Override de palace path: `--palace <path>` en cualquier comando.
- Env vars globales: `MEMPALACE_PALACE_PATH`, `MEMPAL_DIR` (auto-mining en hooks), `MEMPALACE_MAX_BACKUPS`, `MEMPALACE_BACKEND`.

## 7. Nota para otras instancias de IA
- Esta página NO menciona `compress` — no es un setting, es comando aparte (ver 06-reference-cli.md).
- `MEMPAL_DIR` es clave para automatizar: si está seteada, los hooks auto-minan esa carpeta en cada guardado.
