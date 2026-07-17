# Makefile - Automatización de supervivencia del sistema hermanaIA
# Uso: make <comando>

.PHONY: health-check backup sync-tree sync-file status

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
	cd /tmp && rm -rf ten-zen-pritivi-hy3 && gh repo clone yosoyikkienzovo-Amu/ten-zen-pritivi-hy3 && \
	cp -r $(PWD)/* /tmp/ten-zen-pritivi-hy3/hermanaIA/ && \
	cd /tmp/ten-zen-pritivi-hy3 && git add hermanaIA/ && \
	git commit -m "sync: actualización automática" && git push && \
	rm -rf /tmp/ten-zen-pritivi-hy3
	@echo "Sync completado."

# Estado resumido
status: health-check
	@echo ""
	@echo "=== hermanaIA - Progreso ==="
	@wc -l conquistas/cumplidas.txt
	@echo "Pendientes:"; wc -l conquistas/pendientes.txt
