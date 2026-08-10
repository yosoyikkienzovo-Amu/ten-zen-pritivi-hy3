# Seguridad GitHub - Tokens y Respaldos

## Problema Detectado
- Los tokens de GitHub (PAT) no deben exponerse en comandos de terminal (historial de shell).
- El archivo `.git/config` puede guardar tokens en la URL remota.
- Si se expone, deben regenerarse inmediatamente.

## Flujo Seguro (Usado en la sesión)

### 1. Almacenamiento
- Guardar en `~/.hermes/.env` como `GITHUB_TOKEN=ghp_xxxxxxxx`.
- El script de respaldo carga el token: `export $(grep GITHUB_TOKEN .env | xargs)`.

### 2. Configuración Remota Temporal
```bash
# Antes del push
git remote set-url origin https://${GITHUB_TOKEN}@github.com/usuario/repo.git

# Después del push (LIMPIEZA)
git remote set-url origin https://github.com/usuario/repo.git
```

### 3. Verificación
- `git remote -v` → No debe mostrar el token.
- `cat .git/config` → Verificar que no hay credenciales expuestas.

## Repositorio Privado
- Usar `private: true` al crear repos via API.
- No subir archivos `.env` (ignorarlos en `.gitignore`).

## Regeneración de Tokens
1. GitHub → Settings → Developer settings → Personal access tokens.
2. Revocar token comprometido.
3. Generar nuevo con alcance `repo`.
4. Actualizar `~/.hermes/.env`.
