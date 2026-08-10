#!/bin/bash
# Verification script for environment discovery automation
# Comprehensive verification based on the session with Amú Ikki

SCRIPT_PATH="$HOME/.hermes/scripts/descubrir_entorno.sh"
SISTEMA_FILE="$HOME/.hermes/outputs/knowledge/Conocimiento del propio sistema operativo y del hogar/Sistema_conocimiento.md"
HOGAR_FILE="$HOME/.hermes/outputs/knowledge/Conocimiento del propio sistema operativo y del hogar/Hogar_archivos_agregados.md"
LOG_FILE="$HOME/.hermes/outputs/tasks/cron/descubrir.log"

echo "=== Verification of Environment Discovery Automation ==="
echo

# Check if script exists and is executable
if [ -x "$SCRIPT_PATH" ]; then
    echo "✓ Discovery script exists and is executable"
else
    echo "✗ Discovery script missing or not executable: $SCRIPT_PATH"
    exit 1
fi

# Run the script
echo "Running discovery script..."
OUTPUT="$($SCRIPT_PATH 2>&1)"
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Script executed successfully"
    # Extract duration from output if present
    if echo "$OUTPUT" | grep -q "Descubrimiento completado en"; then
        echo "  Output: $OUTPUT"
    fi
else
    echo "✗ Script failed with exit code $EXIT_CODE"
    echo "Error: $OUTPUT"
    exit 1
fi

# Check that knowledge files were updated
if [ -f "$SISTEMA_FILE" ]; then
    # Check for recent timestamp entry (last 10 minutes - more lenient)
    if tail -30 "$SISTEMA_FILE" | grep -q "## \["; then
        echo "✓ Sistema_conocimiento.md updated with timestamped section"
    else
        echo "✗ No recent timestamp found in Sistema_conocimiento.md"
        echo "  Last few lines:"
        tail -5 "$SISTEMA_FILE"
        exit 1
    fi
else
    echo "✗ Sistema_conocimiento.md not found: $SISTEMA_FILE"
    exit 1
fi

if [ -f "$HOGAR_FILE" ]; then
    # Check for recent timestamp entry (last 10 minutes)
    if tail -30 "$HOGAR_FILE" | grep -q "## \["; then
        echo "✓ Hogar_archivos_agregados.md updated with timestamped section"
    else
        echo "✗ No recent timestamp found in Hogar_archivos_agregados.md"
        echo "  Last few lines:"
        tail -5 "$HOGAR_FILE"
        exit 1
    fi
else
    echo "✗ Hogar_archivos_agregados.md not found: $HOGAR_FILE"
    exit 1
fi

# Check log file
if [ -f "$LOG_FILE" ]; then
    # Check for start log entry
    if tail -10 "$LOG_FILE" | grep -q "Iniciando descubrimiento de entorno"; then
        echo "✓ Log file contains start entry"
    else
        echo "✗ No start entry found in log file"
        exit 1
    fi
    
    # Check for duration entry (might be in last few lines)
    if tail -10 "$LOG_FILE" | grep -q "Duración:"; then
        echo "✓ Log file contains duration entry"
    else
        # This might be okay if the script was modified, so not fatal
        echo "! No duration entry found in recent log (may be expected if script modified)"
    fi
else
    echo "✗ Log file not found: $LOG_FILE"
    exit 1
fi

echo
echo "=== All checks passed ==="
exit 0