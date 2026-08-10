---
name: personal-directive-system
description: Sets up a personal directive and memory system for the Hermes agent, inspired by Opencode's architecture, including persistent directives (AGENTS.md), working memory (MEMORY.md), task tracking (conquistas), and auto-loading configuration.
---

# Personal Directive System

## Overview
This skill creates a structured system for self-directed interaction with the Hermes agent, drawing inspiration from the Opencode agent's architecture. It establishes:
- **AGENTS.md**: A persistent file containing master directives (e.g., cognitive breathing protocol, output contract) that is automatically loaded in each session.
- **MEMORY.md**: A working memory file for tracking recent changes, metrics, and self-evaluations between sessions.
- **Conquistas directory**: A structured tracking system for pending tasks, completed tasks, evaluation prompts, and progress logs.
- **Configuration update**: Adds the directive files to the `instructions` list in `config.yaml` so they are loaded automatically.

The system promotes deliberate, measurable, and evolving agent usage through enforced reflection and documentation.

## When to Use
- You want a consistent set of guiding principles that apply to every agent session.
- You wish to track your interactions, tasks, and learning over time.
- You desire a lightweight system for periodic self-evaluation and improvement.
- You want to ensure the agent adheres to a defined quality contract (e.g., verification, actionability, evidence).

## Steps

### 1. Create the persistent directives file (AGENTS.md)
- Path: `~/.hermes/AGENTS.md`
- Content: Include the **Omniversal Master Directive** (10-stage cognitive breathing protocol) and the **Definitive Master Prompt** (9-point output contract + operational rules).
- This file acts as the agent's persistent "brain".

### 2. Create the working memory file (MEMORY.md)
- Path: `~/.hermes/MEMORY.md`
- Content: Template for tracking recent changes, quality metrics, and a log of self-evaluations. It includes space to copy relevant directives from AGENTS.md for quick reference.

### 3. Set up the conquests tracking structure
- Directory: `~/.hermes/conquistas/`
- Files:
  - `pendientes.txt`: List of pending tasks (format: `[FECHA HH:MM] TÍTULO - Descripción | Utilidad`).
  - `cumplidas.txt`: List of completed tasks (same format).
  - `autoevaluacion-prompt.txt`: The 10-question self-evaluation template to be used after changes.
  - `progreso.md`: Narrative log of evolution, including metrics, architectural principles, and verification checklists.
- This system separates permanent directives (alma) from dynamic tracking (ropaje que muda).

### 4. Configure automatic loading
- Edit `~/.hermes/config.yaml` to add under the `agent` section:
  ```yaml
  instructions:
    - AGENTS.md
    - MEMORY.md
  ```
- This ensures both files are loaded as instructions at the start of every session (similar to Opencode's `instructions` field).

### 5. (Optional) Create verification and helper scripts
- Example: `~/.hermes/scripts/verificar_carga_directivas.sh` – a script to confirm that AGENTS.md and MEMORY.md are being loaded correctly in a new session.
- Example: `~/.hermes/scripts/registrar_autoevaluacion.sh` – a script to facilitate the monthly self-evaluation using the template.

### 6. Verify the setup
- Start a new Hermes session (or simulate by checking that the configuration is correct).
- Confirm that the directives are being referenced (you can ask the agent to recite part of the breathing protocol or output contract).
- Check that the conquistas files are present and usable.

## Reference Files
- `references/agents_template.md` – starter template for AGENTS.md with the breathing protocol and output contract.
- `references/memory_template.md` – starter template for MEMORY.md with sections for directives, changes, metrics, and self-evaluation log.
- `references/conquistas_structure/` – directory containing example files for the conquests system:
  - `pendientes.txt`
  - `cumplidas.txt`
  - `autoevaluacion-prompt.txt`
  - `progreso.md`
- `scripts/verificar_carga.sh` – a helper script to verify that the directive files are set up for auto-loading.
- `scripts/plantilla_autoevaluacion.sh` – a script that opens the autoevaluation template in an editor for completion.

## Maintenance Tips
- **Updating Directives**: When you evolve your guiding principles, edit `AGENTS.md` and optionally copy the updated section to `MEMORY.md` under "Directrices Actuales".
- **Using Conquistas**: 
  - Add new tasks to `pendientes.txt` as they arise.
  - When a task is completed, move it to `cumplidas.txt` with a timestamp and brief impact note.
  - Use `autoevaluacion-prompt.txt` after significant changes to record learnings (answer the 10 questions).
  - Update `progreso.md` periodically to reflect milestones and evolving architecture.
- **Configuration Safety**: After editing `config.yaml`, you can verify the `instructions` field is correct by viewing the file.
- **Backup**: Consider adding the `~/.hermes/AGENTS.md`, `~/.hermes/MEMORY.md`, and `~/.hermes/conquistas/` directory to a version control system (e.g., Git) for history and synchronization across machines.
- **Integration with Cron**: This system works well alongside automated environment discovery (see the `environment-discovery-automation` skill) – the directive system governs *how* you interact, while discovery tracks *what* the system is doing.

## Changelog
- 1.0 – Initial creation based on session with user Amú Ikki, adapting their Opencode-inspired system to Hermes Agent.