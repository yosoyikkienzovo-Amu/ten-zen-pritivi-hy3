---
name: deepwiki
description: DeepWiki MCP proporciona documentación basada en IA para repositorios de GitHub con herramientas para leer estructura y contenido de wikis, hacer preguntas sobre repositorios, y administrar sesiones Devin.
homepage: https://mcp.deepwiki.com/mcp
allowedTools: Bash(curl:*)
---

#DeepWiki

DeepWiki MCP proporciona documentación basada en IA para repositorios de GitHub.

Herramientas disponibles:
- read_wiki_structure: obtiene una lista de temas de documentación para un repositorio
- read_wiki_contents: ver la documentación completa sobre un repositorio
- Ask_question: haga cualquier pregunta sobre un repositorio y obtenga una respuesta basada en IA.
- list_available_repos: enumera tus repositorios disponibles (solo modo privado)
- generate_wiki: genera un wiki de código base para un repositorio; utilícelo solo cuando lo solicite explícitamente el usuario (solo modo privado)
- devin_knowledge_manage: administre notas y sugerencias de conocimiento de Devin: enumere, busque, obtenga, cree, actualice, elimine notas, vea la estructura de carpetas, enumere/vea/descarte sugerencias de conocimiento (solo modo privado)
- devin_playbook_manage: administra los libros de jugadas de Devin: enumera, obtiene, crea, actualiza, elimina (solo modo privado)
- devin_schedule_manage: administra sesiones programadas de Devin: enumera, obtiene, crea, actualiza, elimina (solo modo privado)
- devin_session_create: crea una o más sesiones secundarias de Devin (solo modo privado)
- devin_session_interact: administra una sesión de Devin: obtén estado, envía mensajes, suspende/termina/archiva, lee mensajes y archivos adjuntos, administra etiquetas (solo modo privado)
- devin_session_events: inspecciona eventos de sesión: enumera resúmenes, obtiene detalles completos o busca contenidos de eventos (solo modo privado)
- devin_session_search: busca y filtra sesiones de Devin (solo modo privado)
- list_integrations: enumera todas las integraciones nativas y servidores MCP con sus URL de estado y configuración (solo modo privado)


## Inicio rápido

```golpecito
$HOME/.openclaw/skills/deepwiki/scripts/deepwiki.sh <nombre-herramienta> '<json-args>'
```

## Herramientas

### read_wiki_structure

Obtenga una lista de temas de documentación para un repositorio de GitHub.

Argumentos:
repoName: repositorio de GitHub en formato propietario/repositorio (por ejemplo, "facebook/react")

**Parámetros:**
- `repoName` (cadena) (obligatorio)

```golpecito
$HOME/.openclaw/skills/deepwiki/scripts/deepwiki.sh read_wiki_structure '{"repoName":"<repoName>"}'
```

### leer_wiki_contents

Ver documentación sobre un repositorio de GitHub.

Argumentos:
repoName: repositorio de GitHub en formato propietario/repositorio (por ejemplo, "facebook/react")

**Parámetros:**
- `repoName` (cadena) (obligatorio)

```golpecito
$HOME/.openclaw/skills/deepwiki/scripts/deepwiki.sh read_wiki_contents '{"repoName":"<repoName>"}'
```

### hacer_pregunta

Haga cualquier pregunta sobre un repositorio de GitHub y obtenga una respuesta basada en el contexto y basada en IA.

Argumentos:
repoName: repositorio de GitHub o lista de repositorios (máximo 10) en formato propietario/repositorio
Pregunta: La pregunta que hay que hacer sobre el repositorio.

**Parámetros:**
- `repoName` (cadena) (obligatorio)
- `pregunta` (cadena) (obligatorio)

```golpecito
$HOME/.openclaw/skills/deepwiki/scripts/deepwiki.sh ask_question '{"repoName":"<repoName>","question":"<question>"}'
```