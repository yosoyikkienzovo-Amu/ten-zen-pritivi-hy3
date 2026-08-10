# Makefile - Automatización de supervivencia del sistema hermanaIA
# Uso: make <comando>

.PHONY: health-check backup sync-tree sync-file status check-stale dashboard breathe continue ingest query sync-vault palace palace-map palace-sync backup-vector restore-vector memory-status handoff auto-sync

# Verificar integridad del sistema
health-check:
	bash intercambios/health-check.sh

# Crear backup inmediato de AGENTS.md
backup:
	cp AGENTS.md AGENTS.backup.md
	@echo "Backup de AGENTS.md creado."

# Mostrar árbol completo del sistema
tree:
	@echo "=== hermanaIA ==="
	@find . -not -path './node_modules/*' -not -path './MODELLO/*' -not -name 'package*' -not -name '.env' -not -name 'nvidia.json' | sort

# Sincronizar con GitHub (requiere gh autenticado)
sync:
	@echo "Sincronizando hermanaIA con GitHub..."
	cd /tmp && rm -rf ten-zen-pritivi-hy3 && gh repo clone yosoyikkienzovo-Amu/ten-zen-pritivi-hy3 -- --depth 1 && \
	rsync -a --delete \
	  --exclude='venv/' --exclude='__pycache__/' --exclude='*.pyc' \
	  --exclude='embeddings/' --exclude='lancedb/' --exclude='obsidian-vault/.obsidian/' \
	  --exclude='.git/' --exclude='.env' --exclude='node_modules/' \
	  $(PWD)/ /tmp/ten-zen-pritivi-hy3/hermanaIA/ && \
	cd /tmp/ten-zen-pritivi-hy3 && git add hermanaIA/ && \
	git diff --cached --quiet || git commit -m "sync: hermanaIA $$(date +%Y-%m-%d-%H%M)" && \
	git push && \
	rm -rf /tmp/ten-zen-pritivi-hy3
	@echo "Sync completado."

# Detectar tareas obsoletas (>7 días sin avance)
check-stale:
	bash conquistas/auto-deteccion-obsolescencia.sh

# Dashboard de bienestar del sistema
dashboard:
	bash conquistas/dashboard-bienestar.sh

# Protocolo de respiración post-etapa
breathe:
	bash conquistas/automatizacion-respiracion.sh

# Registrar respiración y continuar
continue:
	@echo "$(shell date '+%Y-%m-%d %H:%M')" > conquistas/.opencode-respiracion
	@echo "✅ Respiración registrada. Flujo autorizado para continuar."
	@echo "📋 Pendientes:"
	@grep -v '^#' conquistas/pendientes.txt | grep -v '^$$'

# Estado resumido
status: health-check
	@echo ""
	@echo "=== hermanaIA - Progreso ==="
	@wc -l conquistas/cumplidas.txt
	@echo "Pendientes:"; wc -l conquistas/pendientes.txt

# === MEMORIA SUPERIOR (Fase 2) ===

MS_DIR=memoria-superior
VENV=$(MS_DIR)/venv/bin/activate

# Ingestar archivos en memoria vectorial (recrea la tabla completa)
ingest:
	. $(VENV) && HF_TOKEN=$$(grep HF_TOKEN $(MS_DIR)/.env 2>/dev/null | cut -d= -f2) python3 $(MS_DIR)/scripts/ingest_to_lancedb.py

# Buscar en memoria semántica
query:
	. $(VENV) && HF_TOKEN=$$(grep HF_TOKEN $(MS_DIR)/.env 2>/dev/null | cut -d= -f2) python3 $(MS_DIR)/scripts/query_lancedb.py "$(q)" $(F)

# Sincronizar vault de Obsidian desde LanceDB
sync-vault:
	. $(VENV) && python3 $(MS_DIR)/scripts/sync_vault.py

# Navegar al palacio mental
palace:
	. $(VENV) && python3 $(MS_DIR)/scripts/palace_navigate.py --room "$(room)" $(if $(context),--context)

# Mapa completo del palacio
palace-map:
	. $(VENV) && python3 $(MS_DIR)/scripts/palace_navigate.py --map

# Sincronizar notas del palacio en vault Obsidian
palace-sync:
	. $(VENV) && python3 $(MS_DIR)/scripts/palace_navigate.py --sync-vault

# Backup de la base vectorial LanceDB
backup-vector:
	bash $(MS_DIR)/scripts/backup_vector.sh backup

# Restaurar backup de LanceDB (make restore-vector FILE=ruta)
restore-vector:
	bash $(MS_DIR)/scripts/backup_vector.sh restore $(FILE)

# Listar backups disponibles
list-backups:
	bash $(MS_DIR)/scripts/backup_vector.sh list

# Estado completo de Memoria Superior
memory-status:
	@echo "=== Estado de Memoria Superior ==="
	@echo "Venv: $$([ -d $(MS_DIR)/venv ] && echo 'OK' || echo 'FALTA')"
	@echo "LanceDB: $$([ -d $(MS_DIR)/lancedb ] && echo 'OK' || echo 'VACIO')"
	@ls $(MS_DIR)/obsidian-vault/*/ 2>/dev/null | wc -l | xargs -I{} echo "Notas en vault: {}"
	@ls $(MS_DIR)/scripts/*.sh $(MS_DIR)/scripts/*.py 2>/dev/null | wc -l | xargs -I{} echo "Scripts: {}"

# Handoff multi-agente (para Hermes, Claude Desktop, etc.)
handoff:
	@echo "=== HERMANAIA HANDOFF ==="
	@echo "Tareas pendientes:"
	@grep "^\[.*\] P[0-9]" conquistas/pendientes.txt 2>/dev/null || echo "(ninguna)"
	@echo ""
	@echo "Ultimas conquistas:"
	@tail -3 conquistas/cumplidas.txt 2>/dev/null
	@echo ""
	@echo "Estado salud:"
	@bash conquistas/dashboard-bienestar.sh 2>/dev/null || echo "(dashboard no disponible)"
	@echo ""
	@echo "Spec completo: hermanaIA.spec.md"

# Auto-sync programado a GitHub (cron-safe)
auto-sync:
	bash conquistas/auto-sync.sh
