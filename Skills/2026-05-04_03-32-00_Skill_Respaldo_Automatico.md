# Skill: Respaldo Automático de TEN-ZEN PRITivi HY3
## Fecha y Hora: 2026-05-04 03:32:00
## Descripción:
Skill para automatizar el respaldo de la carpeta `~/.hermes/` en el repositorio GitHub `ten-zen-pritivi-hy3` y disco externo.

## Pasos:
1.  Verificar conexión a internet.
2.  Ejecutar `git add -A` en `~/.hermes/`.
3.  Hacer commit con mensaje "Respaldo automático: [fecha_hora]".
4.  Ejecutar `git push origin main`.
5.  Sincronizar con disco externo usando `rsync -av ~/.hermes/ /mnt/d/Respaldo_Hermes/`.

## Uso:
- Programar con cron job en WSL: `0 2 * * * /home/amu/.hermes/scripts/backup.sh`
- El script `backup.sh` contiene los pasos anteriores.

## Notas:
- Requiere que el PAT de GitHub esté configurado en `~/.hermes/.env` como `GITHUB_TOKEN`.
- El disco externo debe estar montado en `/mnt/d/` (ajustar según corresponda).
