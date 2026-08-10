#!/bin/bash
# automatizacion-respiracion.sh
# Automatización del protocolo de respiración post-etapa
# Uso después de completar una etapa: make breathe
# Verifica la última conquista y muestra la pregunta de respiración

CUMPLIDAS="conquistas/cumplidas.txt"
MARCA=".opencode-respiracion"

echo ""
echo "=== PROTOCOLO DE RESPIRACIÓN COGNITIVA ==="
echo ""

# 1. Verificar que la última conquista esté registrada
ULTIMA=$(grep -oP '^\[\K[^\]]+' "$CUMPLIDAS" 2>/dev/null | tail -1)
[ -z "$ULTIMA" ] && echo "⚠️  No se encontró la última conquista en cumplidas.txt." && exit 1

FECHA=$(echo "$ULTIMA" | cut -d' ' -f1)
HORA=$(echo "$ULTIMA" | cut -d' ' -f2)

echo "📌 Última conquista: ${FECHA} ${HORA}"

# 2. Extraer título de la última entrada
ULTIMO_TITULO=$(grep -oP '^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] \K.*' "$CUMPLIDAS" | tail -1)
echo "📋 ${ULTIMO_TITULO}"

# 3. Contar conquistas totales
TOTAL=$(grep -cP '^\[\d{4}-\d{2}-\d{2}' "$CUMPLIDAS")
echo ""
echo "📊 Total conquistas: $TOTAL"

# 4. Verificar estado del archivo de respiración
if [ -f "$MARCA" ]; then
  ULTIMA_RESPIRACION=$(cat "$MARCA")
  echo "🔄 Última respiración: $ULTIMA_RESPIRACION"
  echo ""
  echo "⚠️  Ya hay una respiración registrada. ¿Ya se procesó la continuación?"
  echo "   Para reiniciar: rm $MARCA"
else
  echo "🫁 Respiración NO registrada aún."
fi

echo ""
echo "═══════════════════════════════════════"
echo "  ¿Autorizas la procedencia de la"
echo "  siguiente etapa/tarea?"
echo "═══════════════════════════════════════"
echo ""
echo "  Si:   make continue   (registra respiración y continúa)"
echo "  No:   detén el flujo y espera instrucciones."
echo ""

exit 0
