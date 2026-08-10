#!/bin/bash
# auto-sync.sh - Sincronización automática con GitHub (cron-safe)
# Uso: bash conquistas/auto-sync.sh
# Log: /tmp/hermanaIA-auto-sync.log

LOCKFILE="/tmp/hermanaIA-sync.lock"
LOGFILE="/tmp/hermanaIA-auto-sync.log"
NOW=$(date "+%Y-%m-%d %H:%M:%S")

# Evitar ejecuciones concurrentes
if [ -f "$LOCKFILE" ] && kill -0 "$(cat "$LOCKFILE")" 2>/dev/null; then
    echo "[$NOW] SKIP: ya hay una sincronización en curso (PID $(cat "$LOCKFILE"))" >> "$LOGFILE"
    exit 0
fi

echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"' EXIT

cd /home/ikki/.config/opencode || { echo "[$NOW] FAIL: no se pudo acceder al directorio" >> "$LOGFILE"; exit 1; }

# Verificar si hay cambios que merezcan sync
ULTIMO_SYNC=$(grep "SYNC OK" "$LOGFILE" 2>/dev/null | tail -1 | grep -oP '\d{4}-\d{2}-\d{2}' | head -1)
CAMBIOS_RECIENTES=$(find AGENTS.md MEMORY.md conquistas/cumplidas.txt -newer "$LOGFILE" 2>/dev/null | wc -l)

if [ "$CAMBIOS_RECIENTES" -eq 0 ] 2>/dev/null; then
    echo "[$NOW] SKIP: sin cambios detectados" >> "$LOGFILE"
    exit 0
fi

# Ejecutar sync
make sync >> "$LOGFILE" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "[$NOW] SYNC OK (exit $EXIT_CODE)" >> "$LOGFILE"
else
    echo "[$NOW] SYNC FAIL (exit $EXIT_CODE)" >> "$LOGFILE"
fi

# Rotar log si excede 500 líneas
LINES=$(wc -l < "$LOGFILE")
if [ "$LINES" -gt 500 ]; then
    tail -100 "$LOGFILE" > "${LOGFILE}.tmp" && mv "${LOGFILE}.tmp" "$LOGFILE"
fi

exit $EXIT_CODE
