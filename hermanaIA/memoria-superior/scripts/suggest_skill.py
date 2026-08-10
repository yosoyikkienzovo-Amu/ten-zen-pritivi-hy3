#!/usr/bin/env python3
"""
Sugiere la skill más relevante para una consulta usando búsqueda semántica.

Uso: python3 suggest_skill.py "consulta del usuario"
     python3 suggest_skill.py "consulta" --top 3 --min-score 0.3

Salida: JSON con las skills sugeridas ordenadas por similitud.
"""
import sys
import json
import argparse
import lancedb
import numpy as np
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from model_utils import cargar_modelo

LANCEDB_DIR = Path.home() / ".config" / "opencode" / "memoria-superior" / "lancedb"
TABLE_NAME = "skill_index"

def cosine_similarity(a, b):
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    return float(np.dot(a, b))

def main():
    parser = argparse.ArgumentParser(description="Sugiere skills por similitud semántica")
    parser.add_argument("query", nargs="?", help="Consulta del usuario")
    parser.add_argument("--top", type=int, default=1, help="Número de resultados (default: 1)")
    parser.add_argument("--min-score", type=float, default=0.0, help="Umbral mínimo de similitud")
    parser.add_argument("--json", action="store_true", help="Salida JSON pura")
    args = parser.parse_args()

    query = args.query or " ".join(sys.argv[1:]).strip()
    if not query:
        print("❌ Uso: suggest_skill.py \"consulta del usuario\"")
        sys.exit(1)

    db_path = str(LANCEDB_DIR)
    if not Path(db_path).exists():
        print("❌ Índice de skills no encontrado. Ejecuta: make build-skill-index")
        sys.exit(1)

    db = lancedb.connect(db_path)
    try:
        tbl = db.open_table(TABLE_NAME)
    except Exception:
        print("❌ Tabla skill_index no existe. Ejecuta: make build-skill-index")
        sys.exit(1)

    df = tbl.to_pandas()
    if df.empty:
        print("❌ El índice de skills está vacío. Ejecuta: make build-skill-index")
        sys.exit(1)

    model = cargar_modelo()
    q_emb = model.encode([query], normalize_embeddings=True)[0]

    results = []
    for _, row in df.iterrows():
        sim = cosine_similarity(q_emb, row["embedding"])
        if sim >= args.min_score:
            results.append({
                "skill_name": row["skill_name"],
                "description": row["description"],
                "similarity": round(sim, 4),
            })

    results.sort(key=lambda x: x["similarity"], reverse=True)
    top = results[:args.top]

    if args.json:
        print(json.dumps({"query": query, "results": top}, ensure_ascii=False, indent=2))
        return

    if not top:
        print("😕 No se encontraron skills relevantes para tu consulta.")
        return

    print(f"\n🎯 SKILL{'S' if len(top) > 1 else ''} SUGERIDA{'S' if len(top) > 1 else ''}:")
    print("-" * 60)
    for i, r in enumerate(top, 1):
        pct = r["similarity"] * 100
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"  {i}. {r['skill_name']} [{bar}] {pct:.0f}%")
        print(f"     📝 {r['description'][:100]}")
        print()
    print("¿Deseas continuar con alguna skill? Responde:")
    print('  "Sí, procede con <nombre-de-la-skill>"')

if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
