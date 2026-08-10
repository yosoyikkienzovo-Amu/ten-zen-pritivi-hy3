# uv-standard-methodology
> Saved: 2026-07-27T13:52:49.454Z
> Tag: config-standard

# Estándar Obligatorio: `uv` como Gestor Único de Python

## Política
**TODA** instalación de paquetes/apps Python debe usar `uv`. Nada de `pip`, `pipx`, `poetry`, `pipenv`, `conda` para nuevos proyectos.

## Principios de Portabilidad
1. **Proyecto = Carpeta autocontenida** con `pyproject.toml` + `uv.lock`
2. **Caché global** en `~/.cache/uv` (reutilizable entre proyectos)
3. **Python gestionado por `uv`** (`uv python install 3.12`) — no del sistema
4. **Entorno virtual en `.venv/`** del proyecto (gitignored)
5. **Ejecución siempre con `uv run`** — nunca `source .venv/bin/activate`

## Flujo Estándar (Nuevo Proyecto)
```bash
uv init mi-proyecto
cd mi-proyecto
uv python install 3.12    # si no existe
uv add requests pandas    # dependencias
uv run python main.py     # ejecutar
```

## Migración de PC / Formateo
```bash
# En PC nueva:
git clone mi-proyecto
cd mi-proyecto
uv sync                   # restaura TODO exacto (python + deps)
uv run python main.py
```

## Comandos Prohibidos ❌
- `pip install` → usar `uv add`
- `pipx install` → usar `uvx`
- `python -m venv` → usar `uv venv`
- `poetry add` → usar `uv add`

## Variables de Entorno Recomendadas (añadir a .bashrc/.zshrc)
```bash
export UV_CACHE_DIR="$HOME/.cache/uv"
export UV_PYTHON_PREFERENCE="managed"  # siempre usar python de uv
```