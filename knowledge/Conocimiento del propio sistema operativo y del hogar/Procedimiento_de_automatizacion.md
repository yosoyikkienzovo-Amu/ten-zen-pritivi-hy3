# Procedimiento de Automatización: Descubrimiento de Entorno

## Objetivo
Automatizar la recolección periódica de información del sistema y del entorno doméstico, almacenándola con marcas de tiempo en archivos de conocimiento para mantener un registro histórico y facilitar auditorías, depuración y mejora continua del agente TEN-ZEN PRITivi HY3.

## Ubicación del Script
- **Ruta**: `~/.hermes/scripts/descubrir_entorno.sh`
- **Permisos**: Ejecutable (`chmod +x`)
- **Funcionalidad**:
  - Recopila datos básicos del sistema (uname, red, servicios, paquetes, disco, memoria, Python/pip).
  - Añade una sección con timestamp `[YYYY-MM-DD HH:MM:SS]` a `Sistema_conocimiento.md`.
  - Lista archivos no estándar del directorio home (excluyendo carpetas de caché y de Hermes) y los registra con formato `[YYYY-MM-DD HH:MM:SS] [CREADO/MODIFICADO/ELIMINADO] ruta – descripción` en `Hogar_archivos_agregados.md`.

## Configuración del Cron
- **Job ID** (actual): `cb09d9c42c62`
- **Nombre**: Descubrimiento entorno
- **Programación**: `0 */6 * * *` (cada 6 horas)
- **Modo**: `no-agent` (el stdout del script se entrega directamente)
- **Entrega**: `local` (salida guardada en el registro de tareas, no enviada a canales externos)
- **Script**: `descubrir_entorno.sh`

## Cómo Consultar los Logs
1. **Lista de trabajos cron**: `hermes cron list`
2. **Log de ejecución**: `~/.hermes/outputs/tasks/cron/descubrir.log`
   - Cada línea contiene `[YYYY-MM-DD HH:MM:SS] Iniciando descubrimiento de entorno`.
3. **Archivos de conocimiento actualizados**:
   - `~/.hermes/outputs/knowledge/Conocimiento del propio sistema operativo y del hogar/Sistema_conocimiento.md`
   - `~/.hermes/outputs/knowledge/Conocimiento del propio sistema operativo y del hogar/Hogar_archivos_agregados.md`

## Verificación de Funcionalidad
- Ejecutar manualmente: `~/.hermes/scripts/descubrir_entorno.sh` → debe imprimir `Descubrimiento completado en YYYY-MM-DD HH:MM:SS` y retornar código 0.
- Revisar que se agregue una nueva sección con timestamp en ambos archivos de conocimiento.
- Confirmar que el log de tareas muestra la entrada de inicio y no hay mensajes de error.

## Mantenimiento y Mejora
- **Rotación de archivos**: considerar limitar el número de líneas o implementar archivado mensual.
- **Notificaciones**: configurar una alerta (correo o archivo) si el script supera un umbral de duración (ej. 30 segundos) o falla.
- **Exclusiones**: ajustar la variable `EXCLUDE_DIRS` en el script para omitir directorios adicionales (snap, flatpak, cachés de navegadores) según sea necesario.
- **Backup**: versionar el script y los archivos de conocimiento en el repositorio GitHub de Hermes (`https://github.com/yosoyikkienzovo-Amu/ten-zen-pritivi-hy3.git`).

## Historial de Cambios
- **2026-07-16**: Creación inicial del script y configuración del cron (dual delivery local/origin).
- **2026-07-16**: Eliminación del job con entrega a origin debido a fallos de Telegram y duplicación de logs; se mantiene únicamente la entrega local.
- **2026-07-16**: Creación de este documento de procedimiento.