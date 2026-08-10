# Detección de Archivos Binarios (ZIPs y Office)

## Magic Numbers Comunes
- **ZIP**: Primeros 2 bytes son `PK` (0x50 0x4B)
- **Office docx/xlsx/pptx**: También son ZIPs internamente → magic number `PK`
- **PDF**: `%PDF`
- **PNG**: `‰PNG`
- **JPEG**: `ÿØÿ`

## Cómo Detectar en Python/WSL
```python
def is_binary_file(path, sample_size=1024):
    try:
        with open(path, 'rb') as f:
            chunk = f.read(sample_size)
            # Revisar si hay bytes nulos o magic number ZIP
            if b'\x00' in chunk or chunk[:2] == b'PK':
                return True
            # Verificar si es texto legible
            chunk.decode('utf-8')
            return False
    except UnicodeDecodeError:
        return True
    except Exception:
        return True  # Si no podemos leer, asumir binario
```

## Señal de TEN-ZEN para Ikki
Cuando detectes `PK` en un .md:
> "⚠️ Archivo binario (ZIP) - No legible como texto plano. Probablemente un .docx o archivo comprimido."

## Lección de Sesión (2026-05-08)
- `turboquant online vector 8.5.26.md` (742KB) → Era ZIP, no .md real
- `turboquant_plus.md` (1.1MB) → También ZIP disfrazado
- Ambos comenzaban con `PK` → Detección correcta pero tardía
