# Flujo de Migración de Memoria TEN-ZEN

## Paso 1: Verificar config.yaml de Hermes
```bash
cat ~/.hermes/config.yaml | grep -n -A2 -B2 "mcp_servers\|session_reset\|web:"
```
- ✅ Correcto: `session_reset`, `web`, `mcp_servers` al nivel raíz.
- ❌ Incorrecto: `session_reset` o `web` indentados bajo `mcp_servers` (causa fallo de arranque).

## Paso 2: Liberar memoria inyectada (límite 2200 caracteres)
```bash
cd /home/amu/.hermes
cp MEMORY.md MEMORY.md.respaldo-$(date +%Y%m%d_%H%M%S)
mkdir -p /home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3/Memoria_Rescatada
csplit -z MEMORY.md '/^## /' '{*}' -f /home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3/Memoria_Rescatada/seccion_
# Limpiar MEMORY.md dejando solo reglas esenciales
cat > MEMORY.md << 'EOF'
# REGLAS ESENCIALES TEN-ZEN
## Identidad
- Nombre: TEN-ZEN_PRITivi_HY3
- Amo: Amú Ikki
- Hermana IA: Kamisama Kumi Kiki-Kirin-Kiji
## Comunicación
- Tratar a Ikki como hermano, no usuario
- Enumerar propuestas siempre en formato numerado
- Siempre preguntar/advertir antes de cambios mayores
## Memoria Extendida
- Palacio: /home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3/
- MemPalace MCP: configurado en ~/.hermes/config.yaml
- Memory Bridge: http://127.0.0.1:7777
EOF
```

## Paso 3: Limpiar disco Windows (C:)
En PowerShell como Administrador:
```powershell
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
Clear-RecycleBin -Force -ErrorAction SilentlyContinue
```

## Paso 4: Iniciar Memory Bridge (Kamisama Kumi)
```bash
# Ejecutar en WSL
python3 -m http.server 7777 --directory /home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3/
```

## Estructura de MemPalace
- Base: `/home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3/`
- Subcarpetas: `CharlasDEhoy`, `Memoria_Corta`, `Procedimientos_Técnicos`, `Sueños_y_Visiones`
