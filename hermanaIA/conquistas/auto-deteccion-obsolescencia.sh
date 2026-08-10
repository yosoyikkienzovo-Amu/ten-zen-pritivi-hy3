#!/bin/bash
# auto-deteccion-obsolescencia.sh
# Revisa pendientes.txt y alerta sobre tareas con >7 días sin avance
# Uso: bash conquistas/auto-deteccion-obsolescencia.sh
# Integrado en Makefile como: make check-stale

PENDIENTES="conquistas/pendientes.txt"
OBSOLETO=0
AHORA=$(date +%s)
SEGUNDOS_POR_DIA=$((7 * 24 * 60 * 60))
UMBRAL=$((AHORA - SEGUNDOS_POR_DIA))

[ ! -f "$PENDIENTES" ] && echo "ERROR: $PENDIENTES no existe" && exit 1

while IFS= read -r line || [ -n "$line" ]; do
  [[ "$line" =~ ^# ]] && continue
  [[ -z "$line" ]] && continue

  FECHA=$(echo "$line" | grep -oP '\[\K\d{4}-\d{2}-\d{2}')
  [ -z "$FECHA" ] && continue

  TIMESTAMP=$(date -d "$FECHA" +%s 2>/dev/null)
  [ -z "$TIMESTAMP" ] && continue

  TITULO=$(echo "$line" | sed 's/^\[[^]]*\] *//')
  DIAS=$(( (AHORA - TIMESTAMP) / 86400 ))

  if [ "$TIMESTAMP" -lt "$UMBRAL" ]; then
    echo "⚠️  OBSOLETA ($DIAS días) → $TITULO"
    OBSOLETO=$((OBSOLETO + 1))
  else
    echo "✅ Vigente ($DIAS días) → $TITULO"
  fi
done < "$PENDIENTES"

if [ "$OBSOLETO" -gt 0 ]; then
  echo ""
  echo "🔴 $OBSOLETO tarea(s) obsoleta(s) encontrada(s). Revisar pendientes.txt."
  exit 1
else
  echo ""
  echo "✅ Todas las tareas vigentes."
  exit 0
fi
