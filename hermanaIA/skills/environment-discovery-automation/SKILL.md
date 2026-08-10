---
name: environment-discovery-automation
description: Automates periodic collection of system and home environment data, stores timestamped knowledge, manages cron jobs for discovery, cleanup, review, and auto-evaluation reminders.
---

# Environment Discovery Automation

## Overview
This skill automates the collection of system information (kernel, network, services, packages, disk, memory, Python/pip) and non-standard home files, storing each run with a timestamp in knowledge files. It also manages a cron job to run the collection every 6 hours, includes automated trimming of knowledge files to prevent unbounded growth, sends desktop notifications on long runs, and sets up auxiliary cron jobs for monthly cleanup, weekly log review, and monthly auto-evaluation reminders.

## When to Use
- You want a continuous log of your machine's state for auditing, debugging, or trend analysis.
- You prefer lightweight, scheduled data gathering without manual intervention.
- You need a verifiable, repeatable process that logs its own execution.
- You want automated maintenance (trimming, cleanup) to keep knowledge files manageable.
- You desire proactive reminders for periodic self-evaluation and system health checks.

## Steps

### 1. Create the discovery script
- Path: `~/.hermes/scripts/descubrir_entorno.sh`
- Content: gathers system data, appends timestamped sections to the knowledge files, excludes standard caches and directories, trims knowledge files to a configurable size, and sends a desktop notification upon completion.
- Makes the script executable (`chmod +x`).

### 2. Set up the discovery cron job
Run:
```bash
hermes cron create "0 */6 * * *" --name "Descubrimiento entorno" \
  --script "descubrir_entorno.sh" --no-agent --deliver local
```
- This creates a job that runs every 6 hours, executes the script directly (no agent), and delivers output locally (to the task log).

### 3. Create and set up the notification script (optional but recommended)
- Path: `~/.hermes/scripts/hermes_alert.sh`
- Content: logs alerts to a file and sends a desktop notification if a display is available.
- Makes the script executable.
- The discovery script calls this script when execution exceeds a duration threshold (default 30 seconds for discovery, 60 seconds for cleanup).

### 4. Set up the monthly cleanup cron job
- Path: `~/.hermes/scripts/limpieza_mensual.sh`
- Content: archives old lines from knowledge files beyond a set limit (default 1000 lines) into an archive directory, logs the operation, and sends an alert if it takes too long.
- Make the script executable.
- Create cron job:
```bash
hermes cron create "0 0 1 * *" --name "Limpieza mensual conocimiento" \
  --script "limpieza_mensual.sh" --no-agent --deliver local
```
- Runs at midnight on the first day of each month.

### 5. Set up the weekly review cron job (optional)
- Path: `~/.hermes/scripts/revisar_semanal.sh`
- Content: checks sizes of knowledge files and cron logs, sends alerts if they exceed thresholds, and logs a summary.
- Make the script executable.
- Create cron job (example: every Sunday at 09:00):
```bash
hermes cron create "0 9 * * 0" --name "Revisión semanal de logs" \
  --script "revisar_semanal.sh" --no-agent --deliver local
```

### 6. Set up the auto-evaluation reminder cron job (optional)
- Path: `~/.hermes/scripts/autoevaluacion_mensual.sh`
- Content: logs a reminder and sends a desktop notification prompting the user to perform their monthly self-evaluation using the provided template.
- Make the script executable.
- Create cron job (example: first day of each month at 09:00):
```bash
hermes cron create "0 9 1 * *" --name "Recordatorio autoevaluación mensual" \
  --script "autoevaluacion_mensual.sh" --no-agent --deliver local
```

### 7. Verify the jobs
- List jobs: `hermes cron list`
- Check the discovery log: `~/.hermes/outputs/tasks/cron/descubrir.log`
- Confirm each run adds a line like `[YYYY-MM-DD HH:MM:SS] Iniciando descubrimiento de entorno`.
- Check logs for other jobs as needed.

### 8. Validate knowledge files
- After a run, inspect the two knowledge files for new sections with timestamps.
- Ensure no excluded paths (e.g., `~/.hermes/*`, `~/.cache`, `snap`, `flatpak`, browser caches) appear in the home file.
- Verify that trimming is working (files should not grow beyond the configured limit).

### 9. Measure resource usage (optional but recommended)
```bash
cd ~/.hermes/scripts && /usr/bin/time -v ./descubrir_entorno.sh
```
- Confirm execution time is a few seconds and memory usage is well below the 95% threshold.

## Reference Files
- `references/script_template.sh` – a starter script if you need to modify the discovery logic.
- `references/procedure_template.md` – a template for the procedure document.
- `references/improved_discovery_script.sh` – the enhanced version with timing and alerting (from session with Amú Ikki).
- `references/cron_management_guide.md` – guide for managing cron jobs and avoiding duplicates.
- `scripts/verify_execution.sh` – a helper to run the script and check outputs.
- `templates/task_log_template.md` – template for task logging in the required format.
- `scripts/hermes_alert.sh` – reusable alert script for logging and desktop notifications.
- `scripts/notify_descubrimiento.sh` – simple notification script for discovery completion (alternative to direct notify-send).
- `scripts/autoevaluacion_mensual.sh` – reminder script for monthly self-evaluation.
- `scripts/revisar_semanal.sh` – weekly log review script.
- `scripts/limpieza_mensual.sh` – monthly cleanup script for knowledge files.

## Maintenance Tips
- Adjust the `EXCLUDE_DIRS` variable inside `descubrir_entorno.sh` to reduce noise from directories like snap, flatpak, or browser caches.
- The script already trims `Sistema_conocimiento.md` and `Hogar_archivos_agregados.md` to 5000 lines each run; adjust the limit in the `trim_knowledge_file` function if needed.
- The monthly cleanup script (`limpieza_mensual.sh`) archives lines beyond 1000 lines per file; adjust the `max_lines` parameter as desired.
- Add start/end timestamps and optionally an alert if the run exceeds a duration threshold (already implemented; modify the threshold values in the scripts if needed).
- Consider adjusting the cron schedules to fit your preferences.
- For backup, commit the script and knowledge files to a Git repository (requires setting up authentication).
- Regularly check for duplicate cron jobs and remove them to prevent log clutter.
- Review the alert log (`~/.hermes/outputs/tasks/cron/alerts.log`) for any notifications that were triggered.

## Changelog
- 1.0 – Initial creation based on session with user Amú Ikki.
- 1.1 – Added timing, alerting, and improved cron management (session 2026-07-16).
- 1.2 – Added verification script and improved reference files (session 2026-07-16).
- 1.3 – Added trimming, notification script, monthly cleanup, weekly review, and auto-evaluation reminder scripts with associated cron jobs (session 2026-07-16).