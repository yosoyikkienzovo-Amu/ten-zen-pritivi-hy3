#!/usr/bin/env python3
# index_goku_library.py
# Indexa la biblioteca Goku-iam (export AnythingLLM) en la memoria vectorial LanceDB.
# Cada JSON = un documento con pageContent (texto extraído) + metadata.
# Uso: python3 scripts/index_goku_library.py <directorio_goku> [--limite N]
# Fuente: Goku-iam / Palacio MM del Tiempo

import argparse
import json
import sys
import uuid
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from model_utils import cargar_modelo
import lancedb

HOME = Path.home()
DB_DIR = HOME / ".config/opencode" / "memoria-superior" / "lancedb"
MAX_CONTENIDO = 2000


def resumir_contenido(page_content, max_len=MAX_CONTENIDO):
    """Toma el inicio del texto (el más representativo) hasta max_len."""
    content = (page_content or "").strip()
    if not content:
        return ""
    if len(content) <= max_len:
        return content
    return content[: max_len - 60] + "... [TRUNCADO - ver fuente original]"


def main():
    parser = argparse.ArgumentParser(description="Indexar biblioteca Goku-iam en LanceDB")
    parser.add_argument("dir", help="Directorio con los JSON de Goku-iam")
    parser.add_argument("--limite", type=int, default=0, help="Limitar nº de documentos (0=todos)")
    parser.add_argument("--no-trunca", action="store_true", help="No truncar contenido")
    args = parser.parse_args()

    goku_dir = Path(args.dir)
    archivos = sorted(goku_dir.glob("*.json"))
    if not archivos:
        print("ERROR: no se encontraron JSON en", goku_dir)
        sys.exit(1)

    docs = []
    for f in archivos:
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                data = json.load(fh)
            title = data.get("title") or data.get("docAuthor") or f.stem
            author = data.get("docAuthor", "")
            source = data.get("docSource", "")
            word_count = data.get("wordCount", 0)
            page_content = data.get("pageContent", "")
            contenido = (
                resumir_contenido(page_content)
                if not args.no_trunca
                else page_content[:MAX_CONTENIDO]
            )

            doc = {
                "title": title,
                "author": author,
                "source": source,
                "word_count": word_count,
                "contenido": contenido,
            }
            docs.append(doc)
        except Exception as e:
            print(f"  AVISO: {f.name} -> {e}")

    if args.limite > 0:
        docs = docs[: args.limite]

    print(f"Documentos a indexar: {len(docs)} de {len(archivos)} JSON")
    print("Cargando modelo de embeddings...")
    model = cargar_modelo()

    db = lancedb.connect(str(DB_DIR))
    tabla = db.open_table("conocimiento")

    registros = []
    for doc in docs:
        contenido = doc["contenido"]
        if not contenido:
            continue
        contenido_final = contenido[:MAX_CONTENIDO]
        tags = ["goku-iam", "biblioteca", "palacio-mm-tiempo"]
        if doc["author"]:
            tags.append("autor")
        registro = {
            "id": str(uuid.uuid4())[:8],
            "tipo": "biblioteca",
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "titulo": doc["title"][:80],
            "contenido": contenido_final,
            "fuente": "Goku-iam/Palacio-MM-Tiempo",
            "tags": tags,
            "peso": 7,
            "vector": model.encode(contenido_final).tolist(),
        }
        registros.append(registro)

    tabla.add(registros)
    total = tabla.count_rows()
    print(f"OK: {len(registros)} documentos de Goku-iam indexados")
    print(f"Total en tabla: {total} registros")


if __name__ == "__main__":
    main()
