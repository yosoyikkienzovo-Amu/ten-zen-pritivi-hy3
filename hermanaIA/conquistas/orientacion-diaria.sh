#!/bin/bash
# orientacion-diaria.sh - Orientación automática al inicio del día
# Consulta el enrutador semántico con las tareas pendientes y deposita
# el resultado en MEMORY.md para que hermanaIA inicie la sesión orientada.
# Uso: bash conquistas/orientacion-diaria.sh
# Log: /tmp/hermanaIA-orientacion.log

LOCKFILE="/tmp/hermanaIA-orientacion.lock"
LOGFILE="/tmp/hermanaIA-orientacion.log"
NOW=$(date "+%Y-%m-%d %H:%M:%S")
OPCODE_DIR="/home/ikki/.config/opencode"
VENV="$OPCODE_DIR/memoria-superior/venv/bin/python3"
ROUTER="$OPCODE_DIR/memoria-superior/scripts/route_memory.py"
MEMORY="$OPCODE_DIR/MEMORY.md"
PENDIENTES="$OPCODE_DIR/conquistas/pendientes.txt"

# Evitar ejecuciones concurrentes
if [ -f "$LOCKFILE" ] && kill -0 "$(cat "$LOCKFILE")" 2>/dev/null; then
    echo "[$NOW] SKIP: orientación en curso" >> "$LOGFILE"
    exit 0
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"' EXIT

# ── FASE 1: Construir el contexto de orientación del día ──
# Toma las primeras tareas PENDIENTES como objetivo del día
CONTEXTO=""
if [ -f "$PENDIENTES" ]; then
    CONTEXTO=$(grep -E "PENDIENTE" "$PENDIENTES" | head -3 | tr '\n' ' ')
fi
[ -z "$CONTEXTO" ] && CONTEXTO="tareas generales de mantenimiento y mejora del sistema hermanaIA"

echo "[$NOW] Contexto del día: $CONTEXTO" >> "$LOGFILE"

# ── FASE 2: Consultar el enrutador ──
RESULTADO=$("$VENV" "$ROUTER" "$CONTEXTO" 2>/dev/null)
EXIT=$?

if [ $EXIT -ne 0 ]; then
    echo "[$NOW] FAIL: enrutador no disponible (exit $EXIT)" >> "$LOGFILE"
    exit 1
fi

# ── FASE 3: Depositar la orientación en MEMORY.md (reemplazo robusto con python) ──
ORIENTACION=$(echo "$RESULTADO" | grep -E "Tarea detectada|SKILLS|skill_name|conocimiento|^  [0-9]" | sed 's/^/    /')

python3 - "$MEMORY" "$ORIENTACION" "$NOW" << 'EOF'
import re
import sys

MEMORY = sys.argv[1]
ORIENTACION = sys.argv[2]
NOW = sys.argv[3]

with open(MEMORY, encoding="utf-8") as f:
    content = f.read()

# Eliminar cualquier bloque ORIENTACIÓN DEL DÍA previo (incluido el título)
content = re.sub(r"\n## ORIENTACIÓN DEL DÍA.*?(?=\n## |\Z)", "", content, flags=re.DOTALL)

# Añadir el nuevo bloque al final
bloque = f"\n## ORIENTACIÓN DEL DÍA ({NOW})\n{ORIENTACION}"
content = content.rstrip() + "\n" + bloque + "\n"

with open(MEMORY, "w", encoding="utf-8") as f:
    f.write(content)
EOF

echo "[$NOW] OK: orientación depositada en MEMORY.md" >> "$LOGFILE"
echo "[$NOW] Orientación diaria completada" >> "$LOGFILE"
exit 0
