---
name: environment_knowledge_automation
description: Automates collection and periodic update of system environment knowledge for TEN-ZEN PRITivi HY3.
version: 1.0.0
author: Hermes Agent + User
metadata:
  hermes:
    tags: [environment, knowledge, automation, cron, monitoring]
    related_skills: [hermes-agent, hermes-agent-skill-authoring]
---

# Environment Knowledge Automation Skill

This skill automates the collection, storage, and periodic updating of system environment knowledge for the TEN-ZEN PRITivi HY3 agent. It creates a knowledge base, a discovery script, and a cron job to keep the information fresh while respecting resource limits (target ~95% usage).

## When to Use
- You want a continuously updated record of the host system (OS, hardware, network, services, packages, storage).
- You want to track user‑added files (non‑system) under `$HOME` and `$HOME/.hermes`.
- You prefer automated, lightweight checks that avoid overloading the agent.

## Steps
1. **Create the knowledge directory** (if it does not exist):
   ```bash
   mkdir -p ~/.hermes/outputs/knowledge/Conocimiento\ del\ propio\ sistema\ operativo\ y\ del\ hogar
   ```
2. **Place the discovery script** (see `scripts/discover_env.sh` template) in `~/.hermes/scripts/` and make it executable.
3. **Run the script once** to seed the knowledge files:
   ```bash
   ~/.hermes/scripts/discover_env.sh
   ```
4. **Schedule periodic execution** (e.g., every 6 hours) with Hermes cron:
   ```bash
   hermes cron create "0 */6 * * *" --script descubrir_entorno.sh --no-agent --name "Entorno descubrimiento"
   ```
5. **Verify** the job with `hermes cron list` and trigger a manual run with `hermes cron run <JOB_ID>`.
6. **Review** the updated markdown files:
   - `Sistema_conocimiento.md` – system‑level facts (timestamped sections).
   - `Hogar_archivos_agregados.md` – user‑added/modified files (timestamped entries).

## Maintenance Tips
- Keep each discovery run under a few seconds to stay well below the 95 % resource target.
- If the script ever exceeds expected time, trim the output (e.g., limit `dpkg -l` to first 30 lines).
- Adjust the cron schedule (`*/6` for every 6 hours) based on how frequently your environment changes.
- The knowledge files are plain Markdown; feel free to edit them manually for notes or to remove obsolete entries.

## Related Files
- `scripts/discover_env.sh` – the discovery script (template).
- `references/example_cron.md` – example cron command variations.