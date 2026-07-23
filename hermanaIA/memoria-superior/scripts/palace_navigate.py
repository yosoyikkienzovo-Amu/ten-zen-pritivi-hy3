#!/usr/bin/env python3
# palace_navigate.py
# Navegacion del Palacio Mental de hermanaIA
# Uso: python3 scripts/palace_navigate.py --room "Vestibulo" [--context]
#      python3 scripts/palace_navigate.py --map

import argparse
import yaml
import lancedb
import sys
import json
from datetime import datetime
from pathlib import Path
from sentence_transformers import SentenceTransformer
from model_utils import cargar_modelo, CACHE_DIR

HOME = Path.home()
BASE = HOME / ".config/opencode"
PALACIO_CONFIG = BASE / "memoria-superior" / "palacio" / "habitaciones.yaml"
DB_DIR = BASE / "memoria-superior" / "lancedb"
CACHE_DIR = BASE / "memoria-superior" / "embeddings"
VAULT_DIR = BASE / "memoria-superior" / "obsidian-vault" / "04 - Palacio"
NAV_LOG = BASE / "memoria-superior" / "palacio" / "navegacion.log"

def cargar_palacio():
    with open(PALACIO_CONFIG, encoding="utf-8") as f:
        return yaml.safe_load(f)

def buscar_conocimientos_por_tags(tags_filtro, limit=5):
    if not tags_filtro or not (DB_DIR / "conocimiento.lance").exists():
        return []
    try:
        db = lancedb.connect(str(DB_DIR))
        if "conocimiento" not in db.list_tables().tables:
            return []
        tabla = db.open_table("conocimiento")
        model = cargar_modelo()
        qv = model.encode(" ".join(tags_filtro)).tolist()
        cond = " OR ".join([f"tags LIKE '%{t}%'" for t in tags_filtro])
        resultados = tabla.search(qv).where(cond).limit(limit).to_pandas()
        return [(r.get("titulo", "?")[:60], r.get("tipo", "?"), r.get("fuente", "?"))
                for _, r in resultados.iterrows()]
    except Exception:
        return []

def navegar(room_name, mostrar_contexto=False):
    palacio = cargar_palacio()
    for h in palacio["habitaciones"]:
        if h["nombre"].lower() == room_name.lower():
            # Registrar navegación
            with open(NAV_LOG, "a") as log:
                log.write(f"{datetime.now().isoformat()} | ENTER | {h['nombre']} | {h.get('icon', '')}\n")
            icon = h.get("icon", "")
            color = h.get("color", "")
            print(f"\n  {icon} \033[1;97m{h['nombre']}\033[0m")
            print(f"  \033[90m{h['descripcion']}\033[0m")
            print(f"  Nivel de acceso: {h.get('nivel_acceso', 0)}")
            print(f"  Conexiones: \033[1;36m{'  ↔  '.join(h['conexiones'])}\033[0m")
            print()
            print(f"  \033[1;97mLoci ({len(h['loci'])} puntos de memoria):\033[0m")
            for i, locus in enumerate(h["loci"], 1):
                print(f"    {i}. {locus}")
            if mostrar_contexto:
                print()
                print(f"  \033[1;97mConocimientos relacionados desde LanceDB:\033[0m")
                conocimientos = buscar_conocimientos_por_tags(h.get("tags_filtro", []))
                if conocimientos:
                    for titulo, tipo, fuente in conocimientos:
                        print(f"    [{tipo}] {titulo} ({fuente})")
                else:
                    print(f"    \033[90m(Sin datos cargados aun)\033[0m")
            return h
    print(f"  Habitacion '{room_name}' no encontrada.")
    return None

def listar_todas():
    palacio = cargar_palacio()
    p = palacio["palacio"]
    print(f"\n  \033[1;97m{p['icon'] if 'icon' in p else '🏰'} {p['nombre']}\033[0m")
    print(f"  Estilo: {p['estilo']}")
    print(f"  Version: {p['version']}")
    print()
    for h in palacio["habitaciones"]:
        icon = h.get("icon", "")
        conecta = " \033[1;36m↔\033[0m ".join(h["conexiones"])
        print(f"  {icon} \033[1;97m{h['nombre']:<20s}\033[0m {h['loci_count'] if 'loci_count' in h else len(h['loci']):>2d} loci  →  {conecta}")

def generar_notas_vault():
    palacio = cargar_palacio()
    VAULT_DIR.mkdir(parents=True, exist_ok=True)

    # Mapa del palacio
    mapa = "# Mapa del Palacio\n\n"
    for h in palacio["habitaciones"]:
        icon = h.get("icon", "")
        conecta = ", ".join(h["conexiones"])
        mapa += f"- {icon} **{h['nombre']}** ({len(h['loci'])} loci) → {conecta}\n"
    (VAULT_DIR / "Mapa del Palacio.md").write_text(mapa, encoding="utf-8")

    # Una nota por habitacion
    for h in palacio["habitaciones"]:
        icon = h.get("icon", "")
        loci_str = "\n".join([f"{i}. {l}" for i, l in enumerate(h["loci"], 1)])
        conexiones_str = "\n".join([f"  - [[04 - Palacio/{c.lower().replace(' ', '-')}|{c}]]" for c in h["conexiones"]])
        nota = f"""---
tipo: habitacion
nombre: {h['nombre']}
nivel_acceso: {h.get('nivel_acceso', 0)}
tags: [{', '.join(h.get('tags_filtro', []))}]
---

# {icon} {h['nombre']}

{h['descripcion']}

## Loci

{loci_str}

## Conexiones

{conexiones_str}
"""
        filename = h["nombre"].lower().replace(" ", "-") + ".md"
        (VAULT_DIR / filename).write_text(nota, encoding="utf-8")

    # Indice
    items = "\n".join([f"1.  [[04 - Palacio/{h['nombre'].lower().replace(' ', '-')}|{h['nombre']}]]" for h in palacio["habitaciones"]])
    indice = f"""---
tipo: indice
carpeta: Palacio
---

# 04 - Palacio

{items}
"""
    (VAULT_DIR / "00 - Índice.md").write_text(indice, encoding="utf-8")
    print(f"Notas del palacio generadas en vault ({len(palacio['habitaciones'])} habitaciones)")

def main():
    parser = argparse.ArgumentParser(description="Palacio Mental de hermanaIA")
    parser.add_argument("--room", help="Nombre de la habitacion")
    parser.add_argument("--map", action="store_true", help="Listar todas las habitaciones")
    parser.add_argument("--context", action="store_true", help="Cargar contexto desde LanceDB")
    parser.add_argument("--sync-vault", action="store_true", help="Generar notas del palacio en Obsidian")
    args = parser.parse_args()

    if args.sync_vault:
        generar_notas_vault()
    elif args.map:
        listar_todas()
    elif args.room:
        navegar(args.room, mostrar_contexto=args.context)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
