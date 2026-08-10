#!/usr/bin/env python3
# add_to_memory.py
# Añade un registro a la memoria vectorial LanceDB (sin recrear la tabla)
# Uso: python3 scripts/add_to_memory.py --titulo "X" --contenido "Y" [--tipo TIPO] [--fuente FUENTE] [--peso N] [--tags a,b,c]

import argparse
import uuid
import sys
from pathlib import Path
from datetime import datetime
from model_utils import cargar_modelo, MODEL_NAME, CACHE_DIR
import lancedb

HOME = Path.home()
DB_DIR = HOME / ".config/opencode" / "memoria-superior" / "lancedb"
CACHE_DIR = HOME / ".config/opencode" / "memoria-superior" / "embeddings"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def inferir_tags(contenido, tipo):
    tags = [tipo]
    low = contenido.lower()
    if "respiracion" in low or "respirar" in low:
        tags.append("respiracion")
    if "seguridad" in low or "backup" in low:
        tags.append("seguridad")
    if "directriz" in low or "directiva" in low or "maestra" in low:
        tags.append("directriz")
    if "palacio" in low or "habitacion" in low:
        tags.append("palacio")
    if "lancedb" in low or "vectorial" in low:
        tags.append("vectorial")
    if "observ" in low or "vault" in low:
        tags.append("obsidian")
    if "make" in low or "comando" in low:
        tags.append("comando")
    if "puente" in low or "intercambio" in low or "externo" in low:
        tags.append("puente")
    if "handoff" in low or "spec" in low or "multi-agente" in low:
        tags.append("coordinacion")
    return list(set(tags))


def main():
    parser = argparse.ArgumentParser(description="Añadir registro a memoria vectorial")
    parser.add_argument("--titulo", required=True, help="Título del registro")
    parser.add_argument("--contenido", required=True, help="Contenido (max 2000 chars)")
    parser.add_argument(
        "--tipo",
        default="memoria_trabajo",
        help="Tipo: directiva, conquista, memoria_trabajo, progreso, sugerencia, tarea, spec, intercambio, reflexion",
    )
    parser.add_argument("--fuente", default="opencode-tool", help="Origen del registro")
    parser.add_argument("--peso", type=int, default=6, help="Peso 1-10")
    parser.add_argument("--tags", default="", help="Tags extra separadas por coma")
    args = parser.parse_args()

    contenido = args.contenido[:2000]
    model = cargar_modelo()

    db = lancedb.connect(str(DB_DIR))
    if "conocimiento" not in db.list_tables().tables:
        print("ERROR: tabla 'conocimiento' no existe. Ejecuta 'make ingest' primero.")
        sys.exit(1)

    tabla = db.open_table("conocimiento")
    extra_tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    all_tags = list(set(inferir_tags(contenido, args.tipo) + extra_tags))

    registro = {
        "id": str(uuid.uuid4())[:8],
        "tipo": args.tipo,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "titulo": args.titulo[:80],
        "contenido": contenido,
        "fuente": args.fuente,
        "tags": all_tags,
        "peso": max(1, min(10, args.peso)),
        "vector": model.encode(contenido).tolist(),
    }

    tabla.add([registro])
    total = tabla.count_rows()
    print(f"OK: registro '{args.titulo[:40]}' añadido (tipo={args.tipo}, peso={args.peso})")
    print(f"Total en tabla: {total} registros")


if __name__ == "__main__":
    main()
