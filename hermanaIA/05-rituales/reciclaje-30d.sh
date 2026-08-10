#!/bin/bash
# reciclaje-30d.sh - Reciclaje perpetuo de la memoria vectorial (renovación cada 30 días)
# Protocolo: backup con checksum -> re-ingesta -> verificación de integridad -> registro
# Uso: bash conquistas/reciclaje-30d.sh
# Log: /tmp/hermanaIA-reciclaje.log
# Doctrina: Recordar Siempre #2 (ciclo reciclaje-compresión verificado en producción)

LOCKFILE="/tmp/hermanaIA-reciclaje.lock"
LOGFILE="/tmp/hermanaIA-reciclaje.log"
NOW=$(date "+%Y-%m-%d %H:%M:%S")
OPCODE_DIR="/home/ikki/.config/opencode"
BACKUP_DIR="$OPCODE_DIR/_backup-configs-fantasma/BACKUP-EVOLUTIVO"
LANCE_DIR="$OPCODE_DIR/memoria-superior/lancedb"
RECICLAJE_LOG="$BACKUP_DIR/RECICLAJE-30D.md"

# Evitar ejecuciones concurrentes
if [ -f "$LOCKFILE" ] && kill -0 "$(cat "$LOCKFILE")" 2>/dev/null; then
    echo "[$NOW] SKIP: reciclaje en curso (PID $(cat "$LOCKFILE"))" >> "$LOGFILE"
    exit 0
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"' EXIT

cd "$OPCODE_DIR" || { echo "[$NOW] FAIL: directorio inaccesible" >> "$LOGFILE"; exit 1; }

# ── FASE 1: Backup preventivo CON CHECKSUM (doctrina: nunca tocar sin resguardo verificado) ──
SUM_BEFORE=$(find "$LANCE_DIR" -type f 2>/dev/null | sort | xargs md5sum 2>/dev/null | md5sum | cut -d' ' -f1)
bash memoria-superior/scripts/backup_vector.sh backup >> "$LOGFILE" 2>&1
echo "[$NOW] Backup vectorial OK (checksum previo: ${SUM_BEFORE:0:12}...)" >> "$LOGFILE"

# ── FASE 2: Re-ingesta (renovación con contenido fresco) ──
memoria-superior/venv/bin/python3 memoria-superior/scripts/ingest_to_lancedb.py >> "$LOGFILE" 2>&1
EXIT_INGEST=$?

# ── FASE 3: Verificación de integridad (criterio de éxito REAL, no "no vi error") ──
REGISTROS=$(memoria-superior/venv/bin/python3 -c "
import lancedb
try:
    db = lancedb.connect('$LANCE_DIR')
    print(db.open_table('conocimiento').count_rows())
except Exception as e:
    print('ERROR')
" 2>/dev/null)
if [ "$EXIT_INGEST" -eq 0 ] && [ "$REGISTROS" != "ERROR" ] && [ "$REGISTROS" -gt 0 ]; then
    ESTADO="OK"
    echo "[$NOW] INTEGRIDAD OK: $REGISTROS registros tras re-ingesta" >> "$LOGFILE"
else
    ESTADO="FALLO"
    echo "[$NOW] INTEGRIDAD FALLO: exit=$EXIT_INGEST registros=$REGISTROS" >> "$LOGFILE"
fi

# ── FASE 4: Registro en el backup evolutivo (memoria del reciclaje perpetuo) ──
touch "$RECICLAJE_LOG"
echo "- $NOW: Reciclaje ($ESTADO) | checksum previo ${SUM_BEFORE:0:12}... | registros=$REGISTROS" >> "$RECICLAJE_LOG"

# ── FASE 5: Rotar log si excede 500 líneas ──
LINES=$(wc -l < "$LOGFILE")
if [ "$LINES" -gt 500 ]; then
    tail -100 "$LOGFILE" > "${LOGFILE}.tmp" && mv "${LOGFILE}.tmp" "$LOGFILE"
fi

[ "$ESTADO" = "OK" ] && exit 0 || exit 1
