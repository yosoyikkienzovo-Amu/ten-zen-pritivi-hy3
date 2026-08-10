# Traducción de Paths: Windows → WSL

## Regla Mental Básica
```
Windows: C:\Users\Ikki\Downloads\archivo.md
WSL:     /mnt/c/Users/Ikki/Downloads/archivo.md
```

## Mapeo de Unidades
| Windows | WSL |
|----------|-----|
| C:\      | /mnt/c/ |
| D:\      | /mnt/d/ |
| E:\      | /mnt/e/ |

## Ejemplos Prácticos

### 1. Descarga simple
```bash
# Windows: C:\Users\Ikki\Downloads\archivo.md
# WSL: /mnt/c/Users/Ikki/Downloads/archivo.md

ls -la "/mnt/c/Users/Ikki/Downloads/"
```

### 2. Ruta con espacios (usar comillas)
```bash
# Windows: C:\Users\Ikki\Downloads\INSTALACIONES pendientes\archivo.md
# WSL: /mnt/c/Users/Ikki/Downloads/INSTALACIONES pendientes/archivo.md

ls -la "/mnt/c/Users/Ikki/Downloads/INSTALACIONES pendientes/"
```

### 3. Conversión automática en TEN-ZEN
```python
def win_to_wsl(path):
    # Reemplazar backslashes
    path = path.replace('\\', '/')
    # Extraer letra de unidad
    if ':' in path:
        drive, rest = path.split(':', 1)
        return f"/mnt/{drive.lower()}{rest}"
    return path
```

## Lección de Sesión (2026-05-08)
**Ruta real leída exitosamente**:
```
Windows: C:\Users\Ikki\Downloads\INSTALACIONESpendientesKLAUDE -otros\TURBO-QUANT\VersionReceinte-SegunKimi\Jigo 8.5.26\
WSL:     /mnt/c/Users/Ikki/Downloads/INSTALACIONESpendientesKLAUDE -otros/TURBO-QUANT/VersionReceinte-SegunKimi/Jigo 8.5.26/
```

**Nota**: Los espacios en nombres de carpetas NO se escapaban en WSL si usamos comillas dobles.
