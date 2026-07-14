# MemPalace — Resumen 02: Mining Your Data

Fuente: https://mempalaceofficial.com/guide/mining.html
Última verificación: 2026-07-13

## 1. Qué es "minar"
Escanear archivos y filar su contenido como "drawers" (cajones) **verbatim** dentro del palace. No resume, no reescribe — guarda el texto exacto.

## 2. Tres modos de minado

### 2.1 Projects (default)
```
mempalace mine ~/projects/myapp
```
- Escanea código, docs, notas. Respeta `.gitignore` por defecto.
- Cada archivo → un drawer, taggeado con **wing** (proyecto) y **room** (tema, auto-detectado en `init`).

Flags útiles:
```
--wing myapp
--no-gitignore
--include-ignored dist,build
--limit 100
--dry-run
```

### 2.2 Conversations (`--mode convos`)
```
mempalace mine ~/chats/ --mode convos
```
Indexa exports de conversación: Claude, ChatGPT, Slack, Markdown, texto plano. Fragmenta por par de intercambio.

### 2.3 General Extraction
```
mempalace mine ~/chats/ --mode convos --extract general
```
Auto-clasifica en 5 tipos: Decisions, Preferences, Milestones, Problems, Emotional context.

## 3. Split de mega-archivos (paso previo obligatorio para convos)
```
mempalace split ~/chats/ --dry-run
mempalace split ~/chats/
mempalace split ~/chats/ --min-sessions 3
mempalace split ~/chats/ --output-dir ~/chats-split/
```
**Regla:** siempre correr `split` antes de minar conversaciones. Es no-op si no hace falta.

## 4. Multi-proyecto (wings)
```
mempalace mine ~/chats/orion/  --mode convos --wing orion
mempalace mine ~/chats/nova/   --mode convos --wing nova
mempalace search "database decision" --wing orion
mempalace search "rate limiting approach"
```

## 5. Agent Tag
```
mempalace mine ~/data/ --agent reviewer
```
Usado por Specialist Agents para particionar memorias.

## 6. Nota para otras instancias de IA
- **No minar todo junto.** Cada proyecto/persona → su propio `--wing`.
- Minado ≠ carga en contexto. Solo indexa en ChromaDB local; nada entra al contexto del LLM hasta `search` o `wake-up`.
- Antes de minar exports de chat: correr `split` primero, siempre.
- `--dry-run` en `mine` y `split` antes de operaciones grandes.
