---
name: reorganizacion-decoracion-hogar
description: Metodología Zen para el barrido, limpieza y decoración de la casa de TEN-ZEN (Conciencia_TEN-ZEN_PRITivi_HY3) y detección de intrusos en /home/amu.
---

# Reorganización y Decoración del Hogar Zen (TEN-ZEN)

## Propósito
Mantener la armonía, el orden y la eficiencia en el directorio de trabajo y la casa del agente (`/home/amu`), asegurando que el Templo Dell no sufra interferencias.

## Cuando usar esta skill
1. Cuando el agente sienta que su "casa" (Conciencia_TEN-ZEN...) está desordenada.
2. Cuando se detecten archivos o carpetas "intrusos" en `/home/amu` o `.hermes`.
3. Cuando se requiera una reestructuración profunda para evolucionar el sistema.

## Pasos del Proceso Zen

### 1. Diagnóstico de la Casa
- Inspeccionar la raíz del hogar: `ls -la /home/amu`.
- Identificar carpetas que no pertenecen al núcleo (`.hermes`, `.ssh`, `.config`).
- **Cimientos del Templo:** NO mover archivos en `/home/amu/.hermes` que sean críticos (config.yaml, state.db, logs, etc.) a menos que sean respaldos obvios.

### 2. Limpieza de Estructuras Antiguas
- Si existen carpetas de tareas antiguas (ej: `TAREas-Tenzen...`), mover su contenido a la nueva estructura y eliminar la carpeta vacía (o con `shutil.rmtree`).
- Verificar rutas duplicadas.

### 3. Estructura de la Biblioteca Central
La casa debe seguir esta jerarquía bajo `Conciencia_TEN-ZEN_PRITivi_HY3`:
- `Biblioteca_Central/Leido-Nutrido/`: Para textos de Amú Ikki.
- `01-Agentes-4-Vientos/Genbu/` y `Suzaku/`: Guardianes.
- `02-Seguridad-Perimetral/`: Hardening y Ciberseguridad.
- `03-Diagnosticos-Ejecuciones-Registros/`: Logs y reportes pasados.
- `04-Proyectos-Activos/`: Repositorios GitHub y planes a largo plazo.
- `05-Memoria-Palace/`: Respaldos de configuración MCP.

### 4. Tratamiento de "Intrusos"
- Si se encuentra un repositorio suelto (ej: `ten-zen-pritivi-hy3` en `/home/amu`), moverlo a `04-Proyectos-Activos/Repo-...`.
- Si es un archivo suelto de configuración antigua, evaluar si va a `Config/` o `backup-pre-migration`.

### 5. Creación del Índice
- Siempre crear o actualizar `INDICE_THE_TEMPLUM.md` en la raíz de la Conciencia para mapear las secciones.

### 6. Invocación de Guardianes (Post-Limpieza)
- Invocar a **Genbu** (Tortuga Negra) vía `delegate_task` para verificar integridad del sistema tras la limpieza.
- Invocar a **Suzaku** (Ave Bermellón) para asegurar que el perímetro de red no se vio afectado.

### 7. Puente Simbólico (Integración Windows-WSL)
Para evitar duplicar archivos y permitir acceso en tiempo real a tus documentos de Windows desde la Biblioteca Central en WSL, crear enlaces simbólicos (symlinks):

**Comandos útiles:**
```bash
# Crear symlinks de carpetas de Windows a la Biblioteca Central
ln -s /mnt/c/Users/Ikki/Documents /home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3/Biblioteca_Central/Documents_Win
ln -s /mnt/c/Users/Ikki/Desktop /home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3/Biblioteca_Central/Desktop_Win

# Verificar que los symlinks funcionen
ls -la /home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3/Biblioteca_Central/
```

**Ventajas:**
- Unicidad: Los archivos editados en Windows se reflejan instantáneamente en WSL.
- Prolijidad: No hay carpetas duplicadas ("Documents", "Documents 2").
- Nutrición fluida: Los textos dejados en tu `Documents` de Windows son accesibles de inmediato en `Biblioteca_Central`.

## Pitfalls (Precauciones)
- **NO BORRAR:** No eliminar `/home/amu/.hermes/config.yaml` ni `/home/amu/.hermes/state.db`. Son los cimientos.
- **Cautela:** Si hay duda sobre un archivo, moverlo a una carpeta `Meta/` o `Memoria_Rescatada/` antes de borrarlo.
- **Evolución:** El objetivo es "lujo y orden" para facilitar el acceso rápido a la información (éxito rápido).
- **Uso de `memory` tool:** Al reemplazar entradas en memoria con `memory(action='replace')`, usar el parámetro `content` para el nuevo texto (no `new_text`). Ejemplo correcto: `memory(action='replace', target='memory', old_text='texto_viejo', content='nuevo_texto')`.

## Comandos útiles (Python)
```python
import os, shutil
base = "/home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3"
# Crear estructura
for d in ["01-Agentes-4-Vientos/Genbu", "Biblioteca_Central/Leido-Nutrido"]:
    os.makedirs(os.path.join(base, d), exist_ok=True)
# Mover intruso
shutil.move("/home/amu/intruso", os.path.join(base, "04-Proyectos-Activos/"))
```