#!/bin/bash
# health-check.sh - Verifica integridad del sistema hermanaIA
# Uso: bash health-check.sh
set -e

DIR="${1:-$HOME/.config/opencode}"
ERRORS=0

echo "=== HEALTH CHECK: hermanaIA ==="
echo "Ruta: $DIR"
echo ""

# 1. Archivos críticos
for f in AGENTS.md MEMORY.md opencode.json; do
  if [ -s "$DIR/$f" ]; then echo "OK  $f ($(wc -l < "$DIR/$f") lines)"
  else echo "FAIL $f missing/empty"; ERRORS=$((ERRORS+1)); fi
done

# 2. Conquistas
for f in pendientes.txt cumplidas.txt progreso.md seguridad-casos-limite.md; do
  if [ -s "$DIR/conquistas/$f" ]; then echo "OK  conquistas/$f"
  else echo "FAIL conquistas/$f"; ERRORS=$((ERRORS+1)); fi
done

# 3. Backup coherente
if diff -q "$DIR/AGENTS.md" "$DIR/AGENTS.backup.md" >/dev/null 2>&1; then
  echo "OK  AGENTS.backup.md (coherente)"
else
  echo "FAIL AGENTS.backup.md (no coincide con AGENTS.md)"
  ERRORS=$((ERRORS+1))
fi

# 4. JSON válido
if python3 -c "import json; json.load(open('$DIR/opencode.json'))" 2>/dev/null; then
  echo "OK  opencode.json (JSON válido)"
else
  echo "FAIL opencode.json (JSON inválido)"
  ERRORS=$((ERRORS+1))
fi

# 5. Gitignore protege archivos sagrados
if grep -q "AGENTS.md" "$DIR/.gitignore" 2>/dev/null; then
  echo "OK  .gitignore protege AGENTS.md"
else
  echo "WARN .gitignore no protege AGENTS.md"
fi

echo ""
echo "=== RESULTADO: $ERRORS errores ==="
exit $ERRORS
