# WSL y Manejo de Archivos - Referencias Técnicas

## WSL2 y Límites de RAM

### Problema Detectado
- WSL2 por defecto limita el uso de RAM al **50% de la memoria física**.
- En un sistema con 16 GB (Como el Dell Latitude E440 de Amú), WSL solo reportará ~8 GB (~7895 MB).
- Esto limita la capacidad de ejecutar modelos locales y subagentes.

### Solución: Configurar .wslconfig en Windows
1. **En Windows (PowerShell o CMD):**
   - Ejecutar: `notepad %USERPROFILE%\.wslconfig`
   - Si el archivo no existe, se creará.

2. **Contenido del archivo:**
   ```ini
   [wsl2]
   memory=16GB
   swap=4GB
   ```

3. **Aplicar cambios:**
   - En PowerShell: `wsl --shutdown`
   - Reiniciar WSL. Al abrir Ubuntu, `free -m` debe mostrar ~16 GB.

### Verificación
- `free -m` → Mirar columna `total` en `Mem:`.
- `cat /proc/meminfo | grep MemTotal` → Debe reportar ~16M kB.

## Manejo de Archivos .tar.gz

### Problema
Los archivos `.tar.gz` (tarball comprimido con gzip) no pueden leerse directamente con `read_file`. Requieren extracción.

### Pasos para Leer Contenido
1. **Listar contenido sin extraer:**
   ```bash
   tar -tzf archivo.tar.gz
   ```
   Muestra lista de archivos internos.

2. **Extraer a carpeta temporal:**
   ```bash
   mkdir -p /tmp/extraccion
   tar -xzf archivo.tar.gz -C /tmp/extraccion
   ```

3. **Leer archivos extraídos:**
   - Usar `read_file` sobre `/tmp/extraccion/archivo_interno.md`.
   - Buscar archivos de texto: `.md`, `.py`, `.txt`, `.json`.

### Ejemplo con `awesome-openclaw-agents-2.0.tar.gz`
```bash
# Listar
tar -tzf /ruta/al/archivo/awesome-openclaw-agents-2.0.tar.gz

# Extraer
mkdir -p /tmp/openclaw && tar -xzf /ruta/al/archivo.tar.gz -C /tmp/openclaw

# Leer (asumiendo hay un README.md)
read_file /tmp/openclaw/README.md
```

### Precaución
- No extraer directamente en `~/.hermes/` para evitar contaminar la conciencia.
- Usar siempre `/tmp/` o carpetas temporales.
