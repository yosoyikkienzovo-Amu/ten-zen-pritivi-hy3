#!/usr/bin/env python3
# sync_vault.py
# Genera vault de Obsidian desde los datos de LanceDB
# Crea notas .md en memoria-superior/obsidian-vault/ con enlaces bidireccionales

import lancedb
import os
import re
from pathlib import Path

HOME = Path.home()
BASE = HOME / ".config/opencode"
DB_DIR = BASE / "memoria-superior" / "lancedb"
VAULT = BASE / "memoria-superior" / "obsidian-vault"

MAP_TIPO_CARPETA = {
    "directiva": "01 - Directrices",
    "memoria_trabajo": "02 - Memoria de Trabajo",
    "conquista": "03 - Conquistas",
    "progreso": "03 - Conquistas",
    "tarea": "03 - Conquistas",
    "sugerencia": "05 - Reflexiones",
}

def slugify(texto):
    texto = texto.lower().strip()
    texto = re.sub(r"\[|\]", "", texto)
    texto = re.sub(r"[áéíóúñ]", lambda m: {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ñ":"n"}[m.group()], texto)
    texto = re.sub(r"[^a-z0-9\s-]", "", texto)
    texto = re.sub(r"[\s-]+", "-", texto)
    return texto[:60]

def generar_frontmatter(r):
    tags = r.get("tags", [])
    if isinstance(tags, list):
        tags_str = "\n  - " + "\n  - ".join(tags) if tags else ""
    else:
        tags_str = f"\n  - {tags}" if tags else ""
    return f"---\ntipo: {r.get('tipo', '?')}\nfecha: {r.get('fecha', '?')}\nfuente: {r.get('fuente', '?')}\npeso: {r.get('peso', '?')}\ntags:{tags_str}\nid: {r.get('id', '?')}\n---\n\n"

def generar_contenido(r):
    contenido = r.get("contenido", "")
    titulo = r.get("titulo", "Sin título")
    lines = contenido.split("\n")
    if len(lines) > 1:
        cuerpo = "\n".join(lines[1:]).strip()
    else:
        cuerpo = contenido
    return f"# {titulo}\n\n{generar_frontmatter(r)}{cuerpo}\n"

def main():
    db = lancedb.connect(str(DB_DIR))
    if "conocimiento" not in db.list_tables().tables:
        print("Base vacía. Ejecuta 'make ingest' primero.")
        return

    tabla = db.open_table("conocimiento")
    df = tabla.to_pandas()
    print(f"Registros en LanceDB: {len(df)}")

    # Limpiar vault (solo notas generadas, no carpetas ni .obsidian)
    for root, dirs, files in os.walk(str(VAULT)):
        for f in files:
            if f.endswith(".md") and f != "00 - Índice.md":
                os.remove(os.path.join(root, f))

    generadas = 0
    indice_notas = {}

    for _, r in df.iterrows():
        tipo = r.get("tipo", "general")
        carpeta = MAP_TIPO_CARPETA.get(tipo, "05 - Reflexiones")
        dir_path = VAULT / carpeta
        dir_path.mkdir(parents=True, exist_ok=True)

        titulo = r.get("titulo", "Sin título")[:80]
        slug = slugify(titulo)
        if not slug:
            slug = r.get("id", "unknown")
        filename = f"{slug}.md"
        filepath = dir_path / filename

        contenido = r.get("contenido", "")
        lines = contenido.split("\n")

        # Construir enlaces a otras notas del mismo tipo
        mismos_tipo = df[df["tipo"] == tipo]
        enlaces = []
        for _, otra in mismos_tipo.iterrows():
            if otra.get("id") == r.get("id"):
                continue
            otro_titulo = otra.get("titulo", "")[:80]
            otro_slug = slugify(otro_titulo)
            otro_carpeta = MAP_TIPO_CARPETA.get(otra.get("tipo", ""), "05 - Reflexiones")
            enlaces.append(f"  - [[{otro_carpeta}/{otro_slug}]]")
        enlaces_str = "\n".join(enlaces[:10]) if enlaces else "  - *(ninguno aún)*"

        tags_raw = r.get("tags", [])
        if hasattr(tags_raw, 'tolist'):
            tags_list = tags_raw.tolist()
        elif isinstance(tags_raw, (list, tuple)):
            tags_list = list(tags_raw)
        else:
            tags_list = []
        tags_str = ", ".join(tags_list) if tags_list else ""

        nota = f"""---
tipo: {tipo}
id: {r.get("id", "?")}
fecha: {r.get("fecha", "?")}
fuente: {r.get("fuente", "?")}
peso: {r.get("peso", "?")}
tags: [{tags_str}]
---

# {titulo}

{r.get("contenido", "")[:2000]}

---
## Enlaces relacionados

{enlaces_str}
"""
        filepath.write_text(nota, encoding="utf-8")
        generadas += 1
        indice_notas.setdefault(carpeta, []).append((titulo, slug))

    # Generar índices por carpeta
    for carpeta in sorted(set(MAP_TIPO_CARPETA.values())):
        dir_path = VAULT / carpeta
        dir_path.mkdir(parents=True, exist_ok=True)
        notas_en_carpeta = indice_notas.get(carpeta, [])
        if notas_en_carpeta:
            items = "\n".join([f"1.  [[{carpeta}/{slug}|{titulo[:60]}]]" for titulo, slug in notas_en_carpeta])
        else:
            items = "*Sin notas aún*"
        index_content = f"""---
tipo: indice
carpeta: {carpeta}
---

# Índice: {carpeta}

Total: {len(notas_en_carpeta)} notas

{items}
"""
        (dir_path / "00 - Índice.md").write_text(index_content, encoding="utf-8")

    # Generar índice raíz del vault
    secciones = ""
    for carpeta in sorted(set(MAP_TIPO_CARPETA.values())):
        count = len(indice_notas.get(carpeta, []))
        secciones += f"\n- [[{carpeta}/00 - Índice|{carpeta}]] ({count} notas)"
    root_index = f"""---
tipo: indice_raiz
---

# hermanaIA — Memoria Superior

Vault de Obsidian generado desde LanceDB.

## Navegación
{secciones}

---
*Generado automáticamente por sync_vault.py*
"""
    (VAULT / "00 - Índice" / "00 - Índice.md").write_text(root_index, encoding="utf-8")

    print(f"Notas generadas: {generadas}")
    print(f"Índices creados: {len(indice_notas)} carpetas")
    print("Vault sincronizado.")

if __name__ == "__main__":
    main()
