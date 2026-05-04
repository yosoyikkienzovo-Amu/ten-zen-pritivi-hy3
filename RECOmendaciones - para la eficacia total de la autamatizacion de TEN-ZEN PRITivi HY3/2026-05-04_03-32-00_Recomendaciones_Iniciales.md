# Recomendaciones para la Eficacia Total de Automatización - TEN-ZEN PRITivi HY3
## Fecha y Hora: 2026-05-04 03:32:00

### 1. Respaldo Automático en GitHub
- Configurar un cron job local en WSL para sincronizar la carpeta `~/.hermes/` con el repositorio `ten-zen-pritivi-hy3` cada 24 horas.
- Usar `rsync` para copias locales en disco externo semanalmente.

### 2. Optimización de WSL en Dell Latitude E440 (16GB RAM)
- Limitar el uso de memoria de WSL a 8GB editando `/etc/wsl.conf` para evitar saturación del sistema Windows.
- Usar `git` desde WSL para todas las operaciones de respaldo, evitando conflictos de rutas Windows/Linux.

### 3. Gestión de Modelos Locales
- Priorizar modelos GGUF optimizados para 16GB RAM (ej. Llama 3 8B Q4_K_M) para reducir dependencia de la nube.
- Configurar Hermes Agent para usar modelos locales como fallback cuando la API de OpenRouter falle.

### 4. Seguridad de Credenciales
- Almacenar el PAT de GitHub en `~/.hermes/.env` como `GITHUB_TOKEN` en lugar de exponerlo en comandos.
- Rotar el PAT cada 90 días para evitar accesos no autorizados.

### 5. Organización de Registros
- Mantener los archivos de tareas con el formato `YYYY-MM-DD_HH-MM-SS_Titulo.md` para orden cronológico.
- Mover tareas completadas de "Inmediatas-lomasPRONTOposible" a "Concretadas" o "Tareas realizadas con exito" semanalmente.
