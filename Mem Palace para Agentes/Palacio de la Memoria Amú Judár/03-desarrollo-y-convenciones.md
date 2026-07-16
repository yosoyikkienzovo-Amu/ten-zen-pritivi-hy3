# 03 — Desarrollo, Convenciones y Contribución

Fuente: material técnico provisto por el usuario (mismo origen que 00). Solo relevante si en algún momento se contribuye código al proyecto MemPalace mismo, no para uso normal de la CLI.
Registrado: 2026-07-13

## 1. Setup de desarrollo
```
uv sync --extra dev   # recomendado; o: pip install -e ".[dev]"
```

## 2. Comandos
```
# Tests
uv run pytest tests/ -v --ignore=tests/benchmarks

# Tests con cobertura
uv run pytest tests/ -v --ignore=tests/benchmarks --cov=mempalace --cov-report=term-missing

# Lint
uv run ruff check .

# Format
uv run ruff format .

# Format check (modo CI)
uv run ruff format --check .
```

## 3. Convenciones
- **Estilo Python:** `snake_case` para funciones/variables, `PascalCase` para clases.
- **Linter:** `ruff`, reglas E/F/W.
- **Formateador:** `ruff format`, comillas dobles.
- **Commits:** Conventional Commits (`fix:`, `feat:`, `test:`, `docs:`, `ci:`).
- **Tests:** `tests/test_*.py`, fixtures en `tests/conftest.py`.
- **Cobertura mínima:** 85% (80% en Windows, por limpieza de file-locking de ChromaDB).

## 4. Nota para otras instancias de IA
- Esto solo aplica si el usuario decide contribuir al repo oficial de MemPalace (PRs upstream) — no es necesario para configurar/usar la instalación local.
- Si se llega a ese punto, usar exactamente estas convenciones (Conventional Commits, ruff, cobertura 85%) para que un PR pase CI sin fricción.
