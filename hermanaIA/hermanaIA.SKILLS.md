# SKILLS & PLUGINS — hermanaIA

## Skills Disponibles
| Skill | Cuando usarlo |
|-------|---------------|
| customize-opencode (built-in) | Editar/crear configuracion de opencode: opencode.json, agentes, subagentes, skills, plugins, MCPs, permisos |
| typer CLI | Escribir/refactorizar CLIs en Python con Typer |

## Plugins
Ninguno adicional instalado.

## MCP Servers
| Servidor | Proposito |
|----------|-----------|
| context7 | Documentacion actualizada de librerias/frameworks SDKs |

## Subagentes (4)
| Agente | Modelo | Rol |
|--------|--------|-----|
| code-engineer | opencode/gpt-5.1-codex | Desarrollo Python (black, isort, pytest) |
| doc-writer | anthropic/claude-sonnet-4-5 | Documentacion tecnica |
| memory-manager | anthropic/claude-haiku-4-5 | Memoria vectorial, archivos obsoletos |
| security-auditor | anthropic/claude-sonnet-4-5 | Seguridad, vulnerabilidades, hardening |

## REGLA: Activacion automatica de skills
Antes de empezar CUALQUIER tarea, revisar:
1. Si la tarea involucra configuracion de opencode → cargar skill `customize-opencode`
2. Si la tarea involucra CLIs en Python con Typer → cargar skill `typer`
3. Si la tarea necesita documentacion de librerias → usar context7 MCP

NUNCA saltarse esta verificacion. Es parte del protocolo de respiracion.
