#!/usr/bin/env python3
# query_lancedb.py
# Búsqueda semántica en memoria vectorial LanceDB
# Uso: python3 scripts/query_lancedb.py "texto de búsqueda" [--limit N] [--tipo TIPO] [--min-peso N]

import argparse
import os
from pathlib import Path
from model_utils import cargar_modelo, MODEL_NAME, CACHE_DIR
import lancedb

HOME = Path.home()
DB_DIR = HOME / ".config/opencode" / "memoria-superior" / "lancedb"
CACHE_DIR = HOME / ".config/opencode" / "memoria-superior" / "embeddings"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

def formatear_resultado(r, score, idx):
    tipo = r.get("tipo", "?")
    titulo = r.get("titulo", "?")
    fuente = r.get("fuente", "?")
    contenido = r.get("contenido", "")[:250]
    peso = r.get("peso", "?")
    tags = r.get("tags", [])
    if isinstance(tags, list):
        tags = ", ".join(tags)
    fecha = r.get("fecha", "?")

    tipo_colors = {
        "directiva": "\033[1;31m",
        "conquista": "\033[1;32m",
        "memoria_trabajo": "\033[1;34m",
        "progreso": "\033[1;33m",
        "sugerencia": "\033[1;35m",
        "tarea": "\033[1;36m",
    }
    reset = "\033[0m"
    color = tipo_colors.get(tipo, "\033[1;37m")

    print(f"\n{'='*60}")
    print(f"  [{idx}] {color}{tipo}{reset} | score: {score:.4f} | peso: {peso}")
    print(f"  {color}{titulo}{reset}")
    print(f"  Fuente: {fuente} | Fecha: {fecha} | Tags: {tags}")
    print(f"{'─'*60}")
    print(f"  {contenido}...")
    return True

def main():
    parser = argparse.ArgumentParser(description="Busqueda semantica en memoria vectorial")
    parser.add_argument("query", nargs="?", help="Texto de búsqueda")
    parser.add_argument("--limit", type=int, default=5, help="Número de resultados (defecto: 5)")
    parser.add_argument("--tipo", help="Filtrar por tipo (directiva, conquista, etc.)")
    parser.add_argument("--min-peso", type=int, default=0, help="Peso mínimo (1-10)")
    parser.add_argument("--raw", action="store_true", help="Salida JSON raw")
    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        return

    model = cargar_modelo()
    db = lancedb.connect(str(DB_DIR))

    if "conocimiento" not in db.list_tables().tables:
        print("Base de datos vacía. Ejecuta 'make ingest' primero.")
        return

    tabla = db.open_table("conocimiento")
    qv = model.encode(args.query).tolist()

    # Construir búsqueda con filtros pre-query (nativo LanceDB)
    busqueda = tabla.search(qv)
    condiciones = []
    if args.tipo:
        condiciones.append(f"tipo = '{args.tipo}'")
    if args.min_peso > 0:
        condiciones.append(f"peso >= {args.min_peso}")
    if condiciones:
        busqueda = busqueda.where(" AND ".join(condiciones))
    resultados = busqueda.limit(args.limit).to_pandas()

    if resultados.empty:
        print(f"Sin resultados con los filtros aplicados.")
        return

    resultados = resultados.head(args.limit)

    if args.raw:
        for _, r in resultados.iterrows():
            print(r.to_json())
        return

    # Mostrar resultados
    print(f"\n\033[1;97m=== BÚSQUEDA: {args.query} ===\033[0m")
    print(f"Resultados: {len(resultados)}")

    for idx, (_, r) in enumerate(resultados.iterrows(), 1):
        score = 1 - r.get("_distance", 0)
        formatear_resultado(r, score, idx)

    # Resumen
    tipos = resultados["tipo"].value_counts()
    print(f"\n\033[1;90mDistribución: ", end="")
    for t, c in tipos.items():
        print(f"{t}:{c} ", end="")
    print("\033[0m")

if __name__ == "__main__":
    main()
