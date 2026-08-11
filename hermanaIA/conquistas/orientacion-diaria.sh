#!/bin/bash
# orientacion-diaria.sh - Orientación automática al inicio del día
# 1) Consulta el enrutador semántico con las tareas pendientes.
# 2) Clasifica las pendientes por peso (PESADA/MEDIANA/PEQUEÑA).
# 3) Propone la PRIORIDAD DEL DÍA (la PESADA más temprana).
# 4) Deposita todo en MEMORY.md para que hermanaIA inicie orientada.
# Uso: bash conquistas/orientacion-diaria.sh
# Log: /tmp/hermanaIA-orientacion.log

LOCKFILE="/tmp/hermanaIA-orientacion.lock"
LOGFILE="/tmp/hermanaIA-orientacion.log"
NOW=$(date "+%Y-%m-%d %H:%M")
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
CONTEXTO=""
if [ -f "$PENDIENTES" ]; then
    CONTEXTO=$(grep -E "PENDIENTE" "$PENDIENTES" | head -3 | tr '\n' ' ')
fi
[ -z "$CONTEXTO" ] && CONTEXTO="tareas generales de mantenimiento y mejora del sistema hermanaIA"

echo "[$NOW] Contexto del día: $CONTEXTO" >> "$LOGFILE"

# ── FASE 1b: Clasificar pendientes por peso y elegir prioridad del día ──
PESADAS=""
MEDIANAS=""
PEQUENAS=""
PRIORIDAD=""
if [ -f "$PENDIENTES" ]; then
    PESADAS=$(grep -E "PENDIENTE \[PESADA\]" "$PENDIENTES" | sed 's/ — PENDIENTE \[PESADA\]//' | tr '\n' '; ')
    MEDIANAS=$(grep -E "PENDIENTE \[MEDIANA\]" "$PENDIENTES" | sed 's/ — PENDIENTE \[MEDIANA\]//' | tr '\n' '; ')
    PEQUENAS=$(grep -E "PENDIENTE \[PEQUEÑA\]" "$PENDIENTES" | sed 's/ — PENDIENTE \[PEQUEÑA\]//' | tr '\n' '; ')
    # Prioridad del día: la PESADA más temprana (en orden del archivo)
    PRIORIDAD=$(grep -E "PENDIENTE \[PESADA\]" "$PENDIENTES" | head -1 | sed 's/ — PENDIENTE \[PESADA\]//')
fi
[ -z "$PRIORIDAD" ] && PRIORIDAD="(sin tareas pesadas pendientes — tomar la primera MEDIANA)"
[ -z "$PESADAS" ] && PESADAS="(ninguna)"
[ -z "$MEDIANAS" ] && MEDIANAS="(ninguna)"
[ -z "$PEQUENAS" ] && PEQUENAS="(ninguna)"

echo "[$NOW] Prioridad del día: $PRIORIDAD" >> "$LOGFILE"

# ── FASE 2: Consultar el enrutador ──
RESULTADO=$("$VENV" "$ROUTER" "$CONTEXTO" 2>/dev/null)
EXIT=$?

if [ $EXIT -ne 0 ]; then
    echo "[$NOW] FAIL: enrutador no disponible (exit $EXIT)" >> "$LOGFILE"
    exit 1
fi

# ── FASE 3: Depositar la orientación en MEMORY.md (reemplazo robusto con python) ──
ORIENTACION=$(echo "$RESULTADO" | grep -E "Tarea detectada|SKILLS|skill_name|conocimiento|^  [0-9]" | sed 's/^/    /')

python3 - "$MEMORY" "$ORIENTACION" "$NOW" "$PRIORIDAD" "$PESADAS" "$MEDIANAS" "$PEQUENAS" << 'EOF'
import re
import sys

MEMORY = sys.argv[1]
ORIENTACION = sys.argv[2]
NOW = sys.argv[3]
PRIORIDAD = sys.argv[4]
PESADAS = sys.argv[5]
MEDIANAS = sys.argv[6]
PEQUENAS = sys.argv[7]

with open(MEMORY, encoding="utf-8") as f:
    content = f.read()

# Eliminar cualquier bloque ORIENTACIÓN DEL DÍA previo (incluido el título)
# Anclado a inicio de línea (MULTILINE) para no tocar punteros en el log vivo
content = re.sub(r"^## ORIENTACIÓN DEL DÍA.*?(?=^## |\Z)", "", content, flags=re.MULTILINE | re.DOTALL)

# Construir el bloque con nuevas líneas reales
prioridad_block = (
    "🎯 PRIORIDAD DEL DÍA (empezar por aquí):\n"
    f"{PRIORIDAD}\n\n"
    "⚖️ TAREAS POR PESO:\n"
    f"  - PESADAS:   {PESADAS}\n"
    f"  - MEDIANAS:  {MEDIANAS}\n"
    f"  - PEQUENAS:  {PEQUENAS}"
)

# Añadir el nuevo bloque al final
bloque = f"\n## ORIENTACIÓN DEL DÍA ({NOW})\n{prioridad_block}\n{ORIENTACION}"
content = content.rstrip() + "\n" + bloque + "\n"

with open(MEMORY, "w", encoding="utf-8") as f:
    f.write(content)
EOF

echo "[$NOW] OK: orientación + prioridad depositadas en MEMORY.md" >> "$LOGFILE"
echo "[$NOW] Orientación diaria completada" >> "$LOGFILE"
exit 0
