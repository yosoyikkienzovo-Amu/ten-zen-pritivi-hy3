#!/bin/bash
# dashboard-bienestar.sh
# Métricas de salud del sistema desde cumplidas.txt
# Uso: bash conquistas/dashboard-bienestar.sh
# Integrado en Makefile como: make dashboard

LC_NUMERIC=C
CUMPLIDAS="conquistas/cumplidas.txt"
[ ! -f "$CUMPLIDAS" ] && echo "ERROR: $CUMPLIDAS no existe" && exit 1

# Extraer timestamps de todas las líneas con [YYYY-MM-DD HH:MM]
TIMESTAMPS=()
while IFS= read -r line || [ -n "$line" ]; do
  if [[ "$line" =~ ^\[([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
    TIMESTAMPS+=("$(date -d "${BASH_REMATCH[1]}" +%s)")
  fi
done < "$CUMPLIDAS"

TOTAL=${#TIMESTAMPS[@]}
[ "$TOTAL" -lt 2 ] && echo "Insuficientes datos para métricas (se necesitan ≥2 entradas)." && exit 1

# Calcular intervalos entre conquistas consecutivas
SUM=0
MIN=${TIMESTAMPS[1]}
MAX=0
INTERVALS=()
for ((i=1; i<TOTAL; i++)); do
  DIFF=$((TIMESTAMPS[i] - TIMESTAMPS[i-1]))
  [ "$DIFF" -lt 0 ] && DIFF=$(( -DIFF ))
  INTERVALS+=("$DIFF")
  SUM=$((SUM + DIFF))
  [ "$DIFF" -lt "$MIN" ] && MIN=$DIFF
  [ "$DIFF" -gt "$MAX" ] && MAX=$DIFF
done

AVG=$((SUM / (TOTAL - 1)))
AVG_HOURS=$((AVG / 3600))
AVG_MIN=$(( (AVG % 3600) / 60 ))

MIN_HOURS=$((MIN / 3600))
MIN_MIN=$(( (MIN % 3600) / 60 ))
MAX_HOURS=$((MAX / 3600))
MAX_MIN=$(( (MAX % 3600) / 60 ))

# Último intervalo (entre las 2 conquistas más recientes)
ULTIMO=${INTERVALS[$((TOTAL - 2))]}
ULT_HOURS=$((ULTIMO / 3600))
ULT_MIN=$(( (ULTIMO % 3600) / 60 ))

# Agrupar por día (sesiones)
declare -A DIAS
for ts in "${TIMESTAMPS[@]}"; do
  DIA=$(date -d "@$ts" +%Y-%m-%d)
  DIAS[$DIA]=$((DIAS[$DIA] + 1))
done

# Buscar errores en cumplidas para ratio de éxito
ERRORES=$(grep -ciP '(error|fail|fallo|bug)' "$CUMPLIDAS" 2>/dev/null || echo 0)
RATIO_EXITO=$(LC_NUMERIC=C echo "scale=1; ($TOTAL - $ERRORES) * 100 / $TOTAL" | bc)

# Rango de fechas
PRIMERA_FECHA=$(date -d "@${TIMESTAMPS[0]}" +%Y-%m-%d)
ULTIMA_FECHA=$(date -d "@${TIMESTAMPS[$TOTAL-1]}" +%Y-%m-%d)

echo "╔══════════════════════════════════════════════╗"
echo "║        DASHBOARD DE BIENESTAR DEL SISTEMA     ║"
echo "╠══════════════════════════════════════════════╣"
echo "║ Total conquistas:    $(printf '%-3s' $TOTAL)                          ║"
echo "║ Rango fechas:        $PRIMERA_FECHA → $ULTIMA_FECHA       ║"
echo "║ Sesiones (días):     $(printf '%-3s' ${#DIAS[@]})                          ║"
CONQ_SESION=$(LC_NUMERIC=C echo "scale=1; $TOTAL / ${#DIAS[@]}" | bc)
echo "║ Conquistas/sesión:   $(printf '%.1f' "$CONQ_SESION") (avg)                    ║"
echo "╠══════════════════════════════════════════════╣"
echo "║ INTERVALOS ENTRE CONQUISTAS                  ║"
echo "║  Promedio:           ${AVG_HOURS}h ${AVG_MIN}m                      ║"
echo "║  Mínimo:             ${MIN_HOURS}h ${MIN_MIN}m                      ║"
echo "║  Máximo:             ${MAX_HOURS}h ${MAX_MIN}m                      ║"
echo "║  Último:             ${ULT_HOURS}h ${ULT_MIN}m                      ║"
echo "╠══════════════════════════════════════════════╣"
echo "║ Ratio éxito:         $RATIO_EXITO% ($ERRORES errores en $TOTAL)      ║"

# === PALACIO MENTAL ===
NAV_LOG="memoria-superior/palacio/navegacion.log"
if [ -f "$NAV_LOG" ]; then
  TOTAL_VISITAS=$(wc -l < "$NAV_LOG")
  HABITACIONES_UNICAS=$(awk -F'|' '{print $3}' "$NAV_LOG" | sort -u | wc -l)
  MAS_VISITADA=$(awk -F'|' '{print $3}' "$NAV_LOG" | sort | uniq -c | sort -rn | head -1 | xargs)
  VISITAS_HOY=$(grep "$(date +%Y-%m-%d)" "$NAV_LOG" | wc -l)
  echo "╠══════════════════════════════════════════════╣"
  echo "║ PALACIO MENTAL                               ║"
  echo "║  Visitas totales:   $(printf '%-3s' $TOTAL_VISITAS)                          ║"
  echo "║  Habitaciones únicas: $(printf '%-3s' $HABITACIONES_UNICAS)                        ║"
  echo "║  Más visitada:      $MAS_VISITADA        ║"
  echo "║  Visitas hoy:       $(printf '%-3s' $VISITAS_HOY)                          ║"
fi

echo "╚══════════════════════════════════════════════╝"
