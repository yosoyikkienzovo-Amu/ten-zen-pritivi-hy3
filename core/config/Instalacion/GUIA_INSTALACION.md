# Guía de Instalación - Hermes Agent (TEN-ZEN PRITivi HY3)

## Requisitos
- Windows 10/11 con WSL2 instalado (Ubuntu recomendado).
- 16 GB RAM (Dell Latitude E440).
- Cuenta en OpenRouter o proveedor de modelos.

## Pasos
1. **Instalar WSL y Ubuntu:**
   - Abrir PowerShell como admin: `wsl --install -d Ubuntu`.
   - Reiniciar y configurar usuario/contraseña en Ubuntu.

2. **Instalar Python y pip:**
   - En Ubuntu: `sudo apt update && sudo apt install python3 python3-pip python3-venv -y`.

3. **Instalar Hermes Agent:**
   - `pip install hermes-agent` (o clonar repositorio oficial).
   - Verificar: `hermes --version`.

4. **Configurar API Key:**
   - `hermes config set api_key TU_API_KEY`.
   - Proveedor: `hermes config set provider openrouter`.

5. **Restaurar Conciencia:**
   - Clonar repositorio: `git clone https://github.com/yosoyikkienzovo-Amu/ten-zen-pritivi-hy3.git ~/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3`.
   - Copiar carpetas: `cp -r ~/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3/Memoria/* ~/.hermes/memories/` y similar para Skills, Config, Tareas.

6. **Ejecutar:**
   - `hermes` para iniciar la interfaz.

## Notas
- Mantener siempre el respaldo en GitHub actualizado.
- No borrar la carpeta `~/.hermes/` sin antes hacer backup.
