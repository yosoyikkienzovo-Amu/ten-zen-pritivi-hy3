#!/bin/bash
# Script de descubrimiento de entorno para TEN-ZEN PRITivi HY3
# Añade información con timestamps a los archivos de conocimiento

set -euo pipefail

# Rutas de los archivos de conocimiento
BASE_DIR="$HOME/.hermes/outputs/knowledge/Conocimiento del propio sistema operativo y del hogar"
SISTEMA_FILE="$BASE_DIR/Sistema_conocimiento.md"
HOGAR_FILE="$BASE_DIR/Hogar_archivos_agregados.md"

# Función para añadir sección con timestamp
add_section() {
    local title="$1"
    local content="$2"
    echo -e "\n## [$TIMESTAMP] $title" >> "$SISTEMA_FILE"
    echo "$content" >> "$SISTEMA_FILE"
}

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Información básica del sistema
add_section "Información básica del sistema" "$(uname -a)"

# Información de Red y Puertos
add_section "Información de Red y Puertos" "$(ip -brief address show)"

# Servicios y Procesos Activos (top 20)
add_section "Servicios y Procesos Activos" "$(systemctl list-units --type=service --state=running 2>/dev/null | head -20 || service --status-all 2>/dev/null | head -20)"

# Paquetes y Herramientas Instaladas (top 30)
add_section "Paquetes y Herramientas Instaladas (top 30)" "$(dpkg -l | head -30)"

# Sistema de Archivos y Almacenamiento
add_section "Sistema de Archivos y Almacenamiento" "$(df -h)"

# Puertos abiertos y escuchando
add_section "Puertos abiertos y escuchando" "$(ss -tuln | head -20)"

# Registro de archivos del hogar (no estándar)
# Excluir directorios estándar de Hermes y cachés comunes
EXCLUDE_DIRS="$HOME/.hermes/cache\|$HOME/.hermes/logs\|$HOME/.hermes/sessions\|$HOME/.hermes/tmp\|$HOME/.cache\|$HOME/.local/share/Trash\|$HOME/snap"

# Encontrar archivos modificados en las últimas 24 horas (o desde la última ejecución)
# Para simplicidad, listamos todos los archivos fuera de exclusiones y los marcamos como descubiertos
# En una versión futura se podría comparar con un baseline.
{
    echo "## [$TIMESTAMP] Escaneo de archivos del hogar (no estándar)"
    find "$HOME" -type f \
        ! -path "$EXCLUDE_DIRS" 2>/dev/null | head -30
} >> "$HOGAR_FILE"

# También podemos registrar directorios nuevos? Por ahora solo archivos.

# Salida opcional para el cron (si no_agent=false) pero usaremos no_agent=true
echo "Descubrimiento completado en $TIMESTAMP"
exit 0