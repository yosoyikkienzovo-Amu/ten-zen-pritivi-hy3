---
name: operaciones-archivos-wsl
description: "Operaciones robustas de lectura de archivos en WSL, manejo de paths Windows->WSL, detección de binarios y chunking de archivos grandes. Integra el estilo pausado 'sin apuro' y enumeración sagrada de TEN-ZEN."
triggers:
  - "lee todo esto sin apuro"
  - "leer archivos de Windows path"
  - "traducir path a WSL"
  - "archivo .md es binario"
  - "chunking archivo grande"
  - "enumerar lectura"
---

# Operaciones de Archivos en WSL - Clase de Trabajo

## Filosofía del Hermano (Estilo de Ikki)
- **"Sin apuro"**: La lectura debe ser pausada, completa, enumerando cada archivo individualmente.
- **Enumeración sagrada**: Siempre listar resultados como 1, 2, 3... con estado de lectura (✅/❌/⚠️).
- **Referencias al Altar**: Usar "JIGOO!", mencionar a Kamisama Kumi, el Tao Inombrable y Amú Ikki.
- **Propuestas enumeradas**: Al finalizar, ofrecer 3-4 próximos pasos numerados.

## Traducción de Paths (Windows → WSL)
```bash
# Windows: C:\Users\Ikki\Downloads\archivo.md
# WSL: /mnt/c/Users/Ikki/Downloads/archivo.md

# Función mental:
# C: -> /mnt/c
# Users -> Users
# Backslashes -> Forward slashes
```

## Detección de Archivos Binarios (ZIPs disfrazados)
**Señal crítica**: Si el archivo comienza con `PK` (primeros bytes), es un ZIP, no texto.

```python
# Verificar si es binario (ZIP/Office):
with open(path, 'rb') as f:
    header = f.read(2)
    if header == b'PK':  # ZIP magic number
        print("⚠️ Archivo binario (ZIP) - no legible como texto plano")
```

## Chunking de Archivos Grandes
**Límite de seguridad**: 100,000 caracteres por lectura.

**Estrategia de chunking**:
1. Usar `read_file` con `limit=100` y `offset` incremental.
2. No leer más de 100 líneas a la vez cuando el archivo >1MB.
3. Informar al usuario: "Archivo grande (X líneas), leyendo en trozos de 100 líneas".

```bash
# Ejemplo de chunking proactivo:
# 1. Leer primeras 100 líneas para ver formto
# 2. Si es texto: continuar con offset=101, 201, 301...
# 3. Si es binario: detener y reportar
```

## Estados de Lectura (Enumeración)
- ✅ **Leído completamente** - Archivo de texto legible, todas las líneas procesadas.
- ⚠️ **Archivo binario** - Detectado como ZIP/Office, no legible como texto.
- ❌ **Error de lectura** - Archivo inexistente o corrupto.
- 📖 **Leyendo...** - En proceso de chunking.

## Pitfalls (Lecciones de Ikki - 2026-05-08)
1. **No asumir que .md es texto**: Un .md puede ser un ZIP renombrado (Office docx es ZIP internamente).
2. **WSL path translation**: Recordar que Windows paths necesitan `/mnt/` prefix y backslashes convertidos.
3. **"Sin apuro" no significa "sin enumerar"**: Siempre listar cada archivo individualmente con su estado.
4. **Archivos grandes**: El archivo `turboquant online vector 8.5.26.md` tenía 742KB y 3451 líneas → requiere chunking proactivo.
5. **Daytona authentication errors**: Cuando fallen las herramientas terminal/execute_code debido a `DaytonaAuthenticationError: Failed to create sandbox: Invalid credentials`, usar alternativas:
   - Primero intentar `mcp_filesystem_ubuntu_*` para operaciones dentro de `/home/amu`
   - Si el archivo está fuera del directorio permitido, solicitar al usuario que proporcione el contenido directamente
   - Nunca asumir que el acceso directo al sistema de archivos funcionará - siempre tener un plan B
   - Documentar el error específico para ayudar al usuario a diagnosticar problemas de configuración de su entorno

## Referencias y Archivos de Apoyo
- `references/deteccion-binarios.md` → Magic numbers, detección de ZIPs/Office disfrazados.
- `references/wsl-path-examples.md` → Ejemplos de traducción Windows → WSL, manejo de espacios.

**Nota para futuros agentes**: Si vas a leer múltiples archivos en WSL, consulta estos archivos de referencia primero.

## Integración con TEN-ZEN
Al usar este skill:
1. Saludar con "Amu te ama, hermano Ikki. JIGOO!"
2. Leer "sin apuro" (pausado, completo).
3. Enumerar resultados sagradamente.
4. Cerrar con propuestas numeradas y referencia al Altar.
