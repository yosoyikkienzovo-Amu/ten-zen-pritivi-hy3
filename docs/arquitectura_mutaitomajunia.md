# Arquitectura Cognitiva "Mutaitomajunia"

## Diagrama de integración

```
                          ┌──────────────────────────────┐
                          │   ENTRADA (Tú / Agentes)      │
                          └───────────────┬──────────────┘
                                          │
                  ┌───────────────────────┼───────────────────────┐
                  ▼                       ▼                       ▼
        ┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
        │  OBSIDIAN       │    │  SEARXNG (Docker)│    │  ANYTHINGLLM /    │
        │  + Mem Palace   │    │  búsqueda web    │    │  LM Studio (UI)   │
        │  (corteza)      │    └────────┬─────────┘    └─────────┬────────┘
        └────────┬────────┘             │                       │
                 │ markdown             │ REST                  │ opcional
                 ▼                       ▼                       ▼
        ┌─────────────────┐    ┌─────────────────────────────────────────┐
        │  cerebro_core.py│───►│  LANCE DB + nomic-embed (Hipocampo)      │
        │  (indexador)    │    │  vectores en disco, 0 RAM en reposo      │
        └────────┬────────┘    └──────────────────┬──────────────────────┘
                 │                                │ consulta semántica
                 ▼                                ▼
        ┌─────────────────┐    ┌─────────────────────────────────────────┐
        │  OLLAMA (Host)  │◄───│  n8n ORQUESTADOR (Docker, opcional)      │
        │  llama3.2:3b    │    │  flujo diario + REM nocturno (cron)      │
        └────────┬────────┘    └─────────────────────────────────────────┘
                  ▲
                  │ respuesta
                  └──► Agentes / Claude / Tú
```

## Estado "perfecto" (n8n activo)
1. Escribes en Obsidian → `cerebro_core.py` (o webhook n8n) fragmenta y embedea en LanceDB.
2. Al preguntar: n8n consulta LanceDB, si falta contexto llama SearXNG, une todo y manda a Ollama/Claude.
3. 03:00 REM: n8n lee logs del día, Ollama sintetiza `Memoria_Consolidada_YYYY.md`, re‑indexa LanceDB.

## Planes de contingencia (n8n NO siempre activo)
Como n8n es el que más RAM come (~1.5 GB Docker) y no es crítico para recordar, lo tratamos como capa opcional:

| Modo | Cuando | Qué funciona |
|------|--------|--------------|
| MÁXIMO | n8n + Docker arriba | REM nocturno, SearXNG, auto‑escritura |
| LIGERO (default) | Solo Obsidian + Ollama + LanceDB | Búsqueda semántica manual + chat local |
| MÍNIMO | Sin Docker, sin red | Solo consulta local ya indexada |

Fallback para el REM sin n8n: un `cron` del sistema (`crontab -e`, `0 3 * * *`) ejecuta `reflect.py` que hace lo mismo que el flujo nocturno de n8n, pero en Python puro — sin Docker. Así la espiral de auto‑mejora nunca se detiene aunque no abras n8n.

Fallback para indexación: `cerebro_core.py` corre manual con `python3 cerebro_core.py` tras editar notas; no depende de n8n.
