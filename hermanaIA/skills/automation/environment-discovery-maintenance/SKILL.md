---
name: environment-discovery-maintenance
category: automation
description: Automate periodic discovery of system and home environment data, maintain knowledge files with size limits, and provide notifications for anomalies.
version: 1.0
---

# Environment Discovery and Maintenance

Automate periodic discovery of system and home environment data, maintain knowledge files with size limits, and provide notifications for anomalies.

## Principles
- Always obtain explicit user authorization before performing any destructive operations (file deletions, system modifications, etc.)
- For discovery and analysis tasks, proceed freely as they are read-only
- When transitioning from analysis to action (cleanup, modification, deletion), require clear, explicit confirmation from the user
- Maintain transparency about what actions will be taken and what data might be affected
- Always systematically map and document the current state of the domain before adding new components or making significant changes
- Value organized, clean systems with clear purpose for each file and directory
- Present options in numbered lists for clear, concise user responses when multiple choices are needed
- Respect user's organizational preferences: when requested, consolidate backups into designated backup folders
- Implement cleanup policies with safeguards against accidental data loss
- For skill management: regularly review skills for utility, eliminate duplicates, and create systems for automatic skill utilization

## Workflow for Safe Operations
1. **Discovery Phase**: Run analysis scripts to map the environment, identify candidates for cleanup/archive (read-only, no authorization needed)
2. **Presentation Phase**: Present findings to user with clear recommendations and options in numbered format for easy response
3. **Authorization Phase**: Obtain explicit user confirmation before executing any destructive operations
4. **Execution Phase**: Perform authorized operations with logging and verification
5. **Verification Phase**: Confirm operations completed as intended and report results

## Safety Guidelines
- Never delete files without explicit user approval
- Always backup configuration files before modification
- Use move-to-quarantine approach when unsure: move candidates to a review folder first
- Maintain clear logs of all actions taken
- Verify disk space availability before creating archives or backups

## Methodology for Domain Mapping
Before making changes to a domain (like ~/.hermes/):
1. Create a comprehensive map of the directory structure including sizes
2. Document the purpose and current state of each significant directory and file
3. Identify duplicates, obsolete items, and noise candidates
4. Present findings with clear recommendations for cleanup, archiving, or retention
5. Only proceed with changes after explicit user authorization

## Specific Procedures from User Preferences

### Configuration Backup Management
When managing configuration file backups:
1. If user requests deletion of all backups: remove all `.bak.*` files
2. Then establish a single backup directory (e.g., `~/hermes/memoria_superior/obsidian_vault/Buck Ups_Todos/`)
3. Implement a rotation policy keeping only the most recent N backups in that directory

### Cache Directory Maintenance
For cache directories (`cache/`, `image_cache/`, `audio_cache/`):
1. Always present analysis of contents before any action
2. Only clear contents with explicit user authorization
3. Consider automated cleanup based on age or size thresholds with user approval

### Skills Directory Optimization
When evaluating the skills directory:
1. Review each skill for recent usage and utility
2. Identify duplicates or obsolete skills
3. Present findings in a structured format for user decision
4. Develop a system for automatic skill recommendation and utilization based on task context

### Log and Snapshot Rotation Policy
For implementing automatic cleanup:
1. Establish a 7-day rotation policy for logs and snapshots
2. Create automation memories in: `~/hermes/memoria_superior/obsidian_vault/Recuerdos de Automatizacion - Hermes/`
3. Use cron jobs or similar scheduling mechanisms
4. Implement fail-safe mechanisms for when systems are offline (e.g., run on startup if missed)
5. Always log actions taken and provide verification mechanisms

## Verification
After implementing any cleanup or organizational changes:
1. Verify that intended files were processed correctly
2. Confirm no unintended deletions or modifications occurred
3. Check that systems continue to function normally
4. Update documentation to reflect changes made

## Workflow for Safe Operations
1. **Discovery Phase**: Run analysis scripts to map the environment, identify candidates for cleanup/archive (read-only, no authorization needed)
2. **Presentation Phase**: Present findings to user with clear recommendations and options
3. **Authorization Phase**: Obtain explicit user confirmation before executing any destructive operations
4. **Execution Phase**: Perform authorized operations with logging and verification
5. **Verification Phase**: Confirm operations completed as intended and report results

## Safety Guidelines
- Never delete files without explicit user approval
- Always backup configuration files before modification
- Use move-to-quarantine approach when unsure: move candidates to a review folder first
- Maintain clear logs of all actions taken
- Verify disk space availability before creating archives or backups
- Always obtain explicit user authorization before performing any destructive operations (file deletions, system modifications, etc.)
- For discovery and analysis tasks, proceed freely as they are read-only
- When transitioning from analysis to action (cleanup, modification, deletion), require clear, explicit confirmation from the user
- Maintain transparency about what actions will be taken and what data might be affected

## When to Use
- You want a regular, automated snapshot of system info (uname, network, services, packages, disk, memory, etc.).
- You want to track non‑standard files in your home directory while excluding known noisy directories (Hermes caches, snap, flatpak, browser caches, etc.).
- You need the knowledge files to stay bounded in size to avoid uncontrolled growth.
- You desire desktop notifications when a run exceeds a time threshold.
- You wish to keep a backup of the scripts and knowledge in a Git repository.

## Steps

### 1. Create the discovery script
Place `~/.hermes/scripts/descubrir_entorno.sh` with the following core components:
- Set `set -euo pipefail`.
- Define paths for knowledge files and log.
- `add_section()` function to prepend a timestamped section to `Sistema_conocimiento.md`.
- `trim_knowledge_file()` function to keep files under a line limit (default 5000).
- Exclude directories via `EXCLUDE_DIRS` (include `.hermes/*`, `.cache`, `snap`, `.var/app`, `.mozilla`, Chrome/Firefox caches, etc.).
- Capture system info via `uname -a`, `ip -brief address show`, `systemctl list-units --type=service --state=running`, `dpkg -l`, `df -h`, `ss -tuln`, `python3 --version`, `pip list`, `free -h`.
- Run a `find $HOME -type f ! -path "$EXCLUDE_DIRS" | awk 'NR<=30'` to collect non‑standard files.
- Log start time, end time, and duration; if duration > 30 s, write an alert to the log and trigger a notification via `hermes_alert.sh`.
- After logging, call `trim_knowledge_file` on both knowledge files.
- Output a completion timestamp (for cron delivery) and optionally invoke a desktop notification script.

### 2. Make the script executable
```bash
chmod +x ~/.hermes/scripts/descubrir_entorno.sh
```

### 3. Create the notification helper
`~/.hermes/scripts/hermes_alert.sh`:
```bash
#!/bin/bash
ALERT_FILE="$HOME/.hermes/outputs/tasks/cron/alerts.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
mkdir -p "$(dirname "$ALERT_FILE")"
echo "[$TIMESTAMP] $1" >> "$ALERT_FILE"
if [ -n "$DISPLAY" ] && command -v notify-send >/dev/null 2>&1; then
    urgency="${2:-normal}"
    notify-send "Hermes Alert" "$1" -u "$urgency" -i dialog-warning
fi
```
Make it executable.

### 4. Create the monthly cleanup script
`~/.hermes/scripts/limpieza_mensual.sh`:
- Similar setup (set -euo pipefail, paths, log file, archive directory).
- `process_file()` function that, if a knowledge file exceeds `max_lines` (default 1000), archives the oldest lines to a timestamped file under `.../archivo/` and keeps only the newest `max_lines`.
- Log archiving actions; if the cleanup exceeds 60 s, log an alert and send a high‑urgency notification.
- Output a completion timestamp.

Make it executable.

### 5. Schedule the discovery cron job
```bash
hermes cronjob create \
  --name "Descubrimiento entorno" \
  --schedule "0 */6 * * *" \
  --script "descubrir_entorno.sh" \
  --no-agent true \
  --deliver "local"
```
- Runs every six hours.
- `no-agent:true` ensures the script’s stdout is delivered directly (the completion message).
- Delivery set to `local` to avoid external notification failures.

### 6. Schedule the monthly cleanup cron job
```bash
hermes cronjob create \
  --name "limpieza_mensual_conocimiento" \
  --schedule "0 0 1 * *" \
  --script "limpieza_mensual.sh" \
  --no-agent true \
  --deliver "local"
```
- Runs at midnight on the first day of each month.

### 7. Backup to GitHub (optional but recommended)
- After verifying the scripts and knowledge files are correct, push them to a remote repository:
  ```bash
  cd /tmp
  git clone https://github.com/yosoyikkienzovo-Amu/ten-zen-pritivi-hy3.git
  cp -r ~/.hermes/scripts/descubrir_entorno.sh ~/.hermes/scripts/hermes_alert.sh ~/.hermes/scripts/limpieza_mensual.sh \
        ~/.hermes/outputs/knowledge/Conocimiento\ del\ propio\ sistema\ operativo\ y\ del\ hogar/ /path/to/cloned/repo/
  cd /path/to/cloned/repo
  git add .
  git commit -m "Update discovery and maintenance scripts"
  git push
  ```
- Automate this step with a separate cron job if desired.

### 8. Create an auto‑evaluation prompt
- See `~/.hermes/outputs/knowledge/Autoevaluación/Prompt_de_autoevaluacion.md` for a structured self‑review template.
- Use it periodically (e.g., monthly) to reflect on the effectiveness of the automation, adjust thresholds, exclusions, or scheduling.

## Pitfalls & How to Avoid Them
- **Duplicate cron jobs**: Always run `hermes cronjob list` before creating a new job; remove duplicates with `hermes cronjob remove <job_id>`.
- **Missing exclusions**: If you see paths like `~/.cache`, `~/snap`, or browser caches appearing in `Hogar_archivos_agregados.md`, update the `EXCLUDE_DIRS` variable in `descubrir_entorno.sh` and re‑run.
- **Scripts not executable**: Forgetting `chmod +x` leads to “Permission denied” in cron logs. Verify after each edit.
- **No‑agent vs agent mode**: If you accidentally create a job with `no_agent:false`, the cron delivery may try to send output to a chat platform and fail, producing error logs. Keep `no_agent:true` for pure‑script jobs.
- **Unbounded file growth**: Without the trimming function, knowledge files will grow indefinitely. Ensure `trim_knowledge_file` is called each run.
- **Incorrect paths**: The monthly archive script must use `"$(basename "$file")"` to avoid `basename: extra operand` errors when paths contain spaces.
- **Notification failures**: If `notify-send` is unavailable (e.g., headless server), the script will still log to `alerts.log`. Test the alert script manually.

## Verification
1. Run the discovery script manually: `~/.hermes/scripts/descubrir_entorno.sh`. Check that:
   - A timestamped section appears in `Sistema_conocimiento.md`.
   - `Hogar_archivos_agregados.md` gains a new section with file list.
   - No excluded paths appear in that list.
   - `~/.hermes/outputs/tasks/cron/descubrir.log` contains start and end timestamps.
   - If runtime >30 s, an alert line and a desktop notification (if possible) are generated.
2. Run the monthly cleanup script manually and verify:
   - The log (`limpieza_mensual.log`) shows archiving actions when files exceed the limit.
   - Archived files appear under `.../archivo/`.
   - Knowledge files are trimmed to the configured line count.
3. Confirm cron jobs:
   ```bash
   hermes cronjob list
   ```
   Look for the two jobs with correct schedules, scripts, and `no_agent:true`.
4. (Optional) Test the alert script:
   ```bash
   ~/.hermes/scripts/hermes_alert.sh "Test message" low
   ```
   Verify a line appears in `alerts.log` and a desktop notification pops up if you are in a graphical session.

## Maintenance
- Review the `EXCLUDE_DIRS` list quarterly or when you install new software that creates noisy cache directories.
- Adjust the line‑count limits (`5000` for discovery logs, `1000` for monthly archive) if you notice the files growing too fast or too slow.
- Keep the backup repository in sync after any script or knowledge‑file changes.

## References
- `references/scripts.md` – brief descriptions of each script and its purpose.
- `templates/knowledge_file_header.md` – example of the timestamped section format used in the knowledge files.