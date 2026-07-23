#!/bin/bash
# backup_vector.sh
# Backup y restore de la base vectorial LanceDB
# Uso: bash scripts/backup_vector.sh [backup|restore ARCHIVO]

MS_DIR="$HOME/.config/opencode/memoria-superior"
LANCEDB_DIR="$MS_DIR/lancedb"
BACKUP_DIR="$MS_DIR/backup"

case "${1:-backup}" in
  backup)
    mkdir -p "$BACKUP_DIR"
    FECHA=$(date +%Y-%m-%d_%H%M)
    ARCHIVO="$BACKUP_DIR/lancedb-backup-$FECHA.tar.gz"
    if [ -d "$LANCEDB_DIR" ] && [ "$(ls -A "$LANCEDB_DIR" 2>/dev/null)" ]; then
      tar -czf "$ARCHIVO" -C "$MS_DIR" lancedb/
      echo "Backup creado: $ARCHIVO ($(du -h "$ARCHIVO" | cut -f1))"
    else
      echo "No hay datos en lancedb/ para backup."
      exit 1
    fi
    ;;
  restore)
    ARCHIVO="${2}"
    if [ -z "$ARCHIVO" ]; then
      echo "Uso: $0 restore <archivo.tar.gz>"
      ls -lh "$BACKUP_DIR" 2>/dev/null
      exit 1
    fi
    if [ ! -f "$ARCHIVO" ]; then
      echo "Archivo no encontrado: $ARCHIVO"
      exit 1
    fi
    rm -rf "$LANCEDB_DIR"
    tar -xzf "$ARCHIVO" -C "$MS_DIR"
    echo "Restaurado desde: $ARCHIVO"
    ls "$LANCEDB_DIR"/ 2>/dev/null
    ;;
  list)
    echo "Backups disponibles:"
    ls -lh "$BACKUP_DIR"/lancedb-backup-*.tar.gz 2>/dev/null || echo "(ninguno)"
    ;;
  *)
    echo "Uso: $0 [backup|restore ARCHIVO|list]"
    ;;
esac
