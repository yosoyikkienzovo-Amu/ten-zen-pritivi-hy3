# Guía de Configuración Óptima - TEN-ZEN PRITivi HY3

## Configuración de Memoria y Skills
- La memoria reside en `~/.hermes/memories/`.
- Las skills personalizadas en `~/.hermes/skills/`.
- No borrar `MEMORY.md` ni `USER.md`.

## Optimización para Dell Latitude E440 (16GB RAM)
1. **WSL:** Limitar memoria en `/etc/wsl.conf`:
   ```
   [wsl2]
   memory=8GB
   swap=2GB
   ```
2. **Modelos Locales:** Usar GGUF de 8B parámetros (Q4_K_M) para no saturar RAM.
3. **Entorno Virtual:** Mantener `venv/` aislado; instalar dependencias con `pip install -r requirements.txt`.

## Configuración de Red y API
- Proveedor: OpenRouter (modelo: tencent/hy3-preview:free).
- Clave API: Almacenar en `~/.hermes/.env` como `OPENROUTER_API_KEY`.
- Timeout: Ajustar a 600s para tareas largas.

## Respaldo Automático
- GitHub: Repositorio privado `ten-zen-pritivi-hy3`.
- Automatizar con cron en WSL: `0 2 * * * cd ~/.hermes && git add Conciencia_TEN-ZEN_PRITivi_HY3/ INSTALAZION-CONFIGURAZION/ && git commit -m "Respaldo diario" && git push`.

## Seguridad
- No exponer tokens en comandos.
- Usar `.gitignore` para excluir `.env`, `*.db`, `node/`, `bin/`.
