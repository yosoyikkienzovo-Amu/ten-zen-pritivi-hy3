#!/bin/bash
# Script de descubrimiento de entorno para TEN-ZEN PRITivi HY3
# Añade información con timestamps a los archivos de conocimiento
# Diseñado para ejecutarse vía cron --no-agent, entregando salida directamente

set -euo pipefail

# Rutas de los archivos de conocimiento
BASE_DIR="$HOME/.hermes/outputs/knowledge/Conocimiento del propio sistema operativo y del hogar"
SISTEMA_FILE="$BASE_DIR/Sistema_conocimiento.md"
HOGAR_FILE="$BASE_DIR/Hogar_archivos_agregados.md"
LOG_FILE="$HOME/.hermes/outputs/tasks/cron/descubrir.log"

# Función para añadir sección con timestamp
add_section() {
    local title="$1"
    local content="$2"
    echo -e "\n## [$TIMESTAMP] $title" >> "$SISTEMA_FILE"
    echo "$content" >> "$SISTEMA_FILE"
}

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Registro de inicio
echo "[$TIMESTAMP] Iniciando descubrimiento de entorno" >> "$LOG_FILE"

# Información básica del sistema
add_section "Información básica del sistema" "$(uname -a)"

# Información de Red y Puertos
add_section "Información de Red y Puertos" "$(ip -brief address show)"

# Servicios y Procesos Activos (limit 20)
add_section "Servicios y Procesos Activos" "$(systemctl list-units --type=service --state=running 2>/dev/null | awk 'NR<=20' || service --status-all 2>/dev/null | awk 'NR<=20')"

# Paquetes y Herramientas Instaladas (top 30)
add_section "Paquetes y Herramientas Instaladas (top 30)" "$(dpkg -l | awk 'NR<=30')"

# Sistema de Archivos y Almacenamiento
add_section "Sistema de Archivos y Almacenamiento" "$(df -h)"

# Puertos abiertos y escuchando
add_section "Puertos abiertos y escuchando" "$(ss -tuln | awk 'NR<=20')"

# Versión de Python y paquetes pip (opcional, ligero)
add_section "Versión de Python y paquetes pip" "$(python3 --version 2>/dev/null || echo 'Python3 no disponible')\\n$(pip list --format=columns 2>/dev/null | awk 'NR<=20' || echo 'pip no disponible o error')"

# Memoria y swap
add_section "Memoria y Swap" "$(free -h)"

# Registro de archivos del hogar (no estándar)
# Excluir directorios estándar de Hermes y cachés comunes
EXCLUDE_DIRS="$HOME/.hermes/cache\|$HOME/.hermes/logs\|$HOME/.hermes/sessions\|$HOME/.hermes/tmp\|$HOME/.cache\|$HOME/.local/share/Trash\|$HOME/snap"

{
    echo "## [$TIMESTAMP] Escaneo de archivos del hogar (no estándar)"
    find "$HOME" -type f \
        ! -path "$EXCLUDE_DIRS" 2>/dev/null | awk 'NR<=30'
} >> "$HOGAR_FILE"

# También registrar directorios nuevos? Por ahora solo archivos.

# Salida opcional para el cron (si no_agent=false) pero usaremos no_agent=true
echo "Descubrimiento completado en $TIMESTAMP"
exit 0