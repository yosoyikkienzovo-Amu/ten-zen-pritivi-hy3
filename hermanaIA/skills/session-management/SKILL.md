---
name: session-management
description: Best practices for managing Hermes sessions, including naming, searching, and cleanup.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [session, productivity, workflow]
---
# Session Management Best Practices

Effective session management makes it easy to resume work, locate past conversations, and keep your Hermes environment organized.

## Why Meaningful Titles Matter

- Default session IDs (e.g., `20260713_221229_d6aa91`) are hard to remember and provide no semantic value.
- A descriptive title lets you quickly recall the topic or goal of a session.
- Titles are searchable via `hermes sessions browse` and `session_search`.

## Setting a Descriptive Title

### During a Session
Use the slash command:
```
/title <Your descriptive title>
```
Example:
```
/title Diagnóstico del sistema
```

### Renaming an Existing Session
From the CLI:
```bash
hermes sessions rename <session-id> "<New Title>"
```
Or by title if unique:
```bash
hermes sessions rename "Diagnóstico del sistema" "Diagnóstico del sistema actualizado"
```

## Finding Sessions Later

### Search by Title or Content
```bash
# Search sessions by keyword in title or messages
session_search(query="diagnóstico", limit=5)
```

### Browse Recent Sessions
```bash
hermes sessions list
hermes sessions browse   # interactive picker
```

## Keeping Your Session List Clean

- **Close unused sessions**: `/quit` or `/exit` ends the session; it remains in history but can be removed.
- **Delete old sessions** when no longer needed:
  ```bash
  hermes sessions delete <session-id>
  ```
- **Prune automatically** (older than N days):
  ```bash
  hermes sessions prune --older-than 30
  ```

## Tips for Consistent Naming

- Use a short phrase that captures the main topic (e.g., “Depuración de API”, “Planificación de proyecto”).
- Avoid using only numbers or timestamps; they add no semantic value.
- If you work on a recurring topic, consider a prefix: `[Proyecto X] Actualización de dependencias`.

## Integration with Other Workflows

- When starting a new task? Begin with `/title` to set context immediately.
- Before ending a session, consider adding a brief summary note via `/title` or a final message summarizing outcomes.
- Use session titles as keys when referencing past work in documentation or skills.

## Real-World Examples from User Session

In a recent session, the user demonstrated these practices:

### Renaming a Cryptic Session ID
Instead of remembering `20260713_221229_d6aa91`, the user renamed it to "Diagnóstico":
```bash
hermes sessions rename 20260713_221229_d6aa91 Diagnóstico
```

### Finding Sessions After Renaming
After renaming, the session was easily located:
```bash
# Search by keyword in session content
session_search(query="Diagnóstico", limit=1)

# Or list all sessions and look for the title
hermes sessions list
```

### Cleaning Up Unnecessary Sessions
Two empty/simple sessions that were just "hola" greetings were removed:
```bash
# First verify what we want to delete
echo y | hermes sessions delete 20260713_172216_f74d44
echo y | hermes sessions delete 20260713_171903_f8daba
```

### Setting a Title During a Session
For future sessions, setting a meaningful title right at the start:
```
/title Diagnóstico del sistema
```

Or renaming later if needed:
```bash
hermes sessions rename "Diagnóstico" "Diagnóstico del sistema actualizado"
```

## Example Workflow

1. Start a new chat: `hermes`  
2. Immediately set title: `/title Investigación de modelos LLM`  
3. Perform your work.  
4. Before exiting, optionally refine title: `/title Investigación de modelos LLM – resultados preliminares`  
5. Later, retrieve: `session_search(query="modelos LLM")`

By following these practices, you’ll spend less time searching for past conversations and more time focusing on the task at hand.

--- 
*This skill captures community‑contributed best practices for Hermes session hygiene. Feel free to extend it with project‑specific conventions.*
2. Immediately set title: `/title Investigación de modelos LLM`  
3. Perform your work.  
4. Before exiting, optionally refine title: `/title Investigación de modelos LLM – resultados preliminares`  
5. Later, retrieve: `session_search(query="modelos LLM")`

By following these practices, you’ll spend less time searching for past conversations and more time focusing on the task at hand.

---  
*This skill captures community‑contributed best practices for Hermes session hygiene. Feel free to extend it with project‑specific conventions.*