#!/usr/bin/env python3
"""
Enrutador Semántico Automático de hermanaIA.

Dado el contexto de la tarea en curso, consulta automáticamente las dos tablas
de memoria (conocimiento + skill_index), clasifica el tipo de tarea y devuelve
lo más relevante para que el agente no pierda tokens decidiendo qué buscar.

Uso: python3 route_memory.py "contexto de la tarea actual"
     python3 route_memory.py "contexto" --top 3 --json

Salida: clasificación + skills sugeridas + fragmentos de memoria pertinentes.
"""

import sys
import json
import argparse
import numpy as np
import lancedb
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from model_utils import cargar_modelo

LANCEDB_DIR = Path.home() / ".config" / "opencode" / "memoria-superior" / "lancedb"
KNOWLEDGE_TABLE = "conocimiento"
SKILL_TABLE = "skill_index"

# Clasificadores léxicos por tipo de tarea (rápidos, sin modelo extra)
TAREA_PATRONES = {
    "codigo": [
        "código",
        "codigo",
        "programar",
        "bug",
        "python",
        "script",
        "función",
        "api",
        "refactor",
        "debug",
        "implementar",
        "desarrollar",
    ],
    "doctrina": [
        "doctrina",
        "colmena",
        "conciencia",
        "colectivizada",
        "brujula",
        "wu-wei",
        "ritual",
        "mision",
        "directiva",
        "agentes",
    ],
    "memoria": [
        "memoria",
        "recordar",
        "lancedb",
        "vectorial",
        "consulta",
        "recuperar",
        "vault",
        "palace",
        "embeddings",
    ],
    "seguridad": [
        "seguridad",
        "secreto",
        "token",
        "clave",
        "permiso",
        "backup",
        "auditar",
        "hardening",
        "vulnerabilidad",
    ],
    "biblioteca": [
        "goku",
        "biblioteca",
        "estudio",
        "esoter",
        "astrolog",
        "alquim",
        "libro",
        "rag",
        "sintesis",
    ],
    "automatizacion": [
        "automatizar",
        "cron",
        "ritual",
        "sync",
        "script",
        "pipeline",
        "tarea programada",
        "workflow",
    ],
    "sistema": [
        "pop",
        "linux",
        "kernel",
        "hardware",
        "ram",
        "disco",
        "cpu",
        "gpu",
        "sistema operativo",
    ],
}


def clasificar_tarea(texto: str) -> str:
    """Clasifica el tipo de tarea por patrones léxicos (primera coincidencia con mayor peso)."""
    low = texto.lower()
    mejor_tipo, mejor_score = "general", 0
    for tipo, patrones in TAREA_PATRONES.items():
        score = sum(1 for p in patrones if p in low)
        if score > mejor_score:
            mejor_tipo, mejor_score = tipo, score
    return mejor_tipo


def cosine_similarity(a, b):
    a = np.asarray(a, dtype=np.float32).flatten()
    b = np.asarray(b, dtype=np.float32).flatten()
    return float(np.dot(a, b))


def main():
    parser = argparse.ArgumentParser(description="Enrutador semántico automático")
    parser.add_argument("query", nargs="?", help="Contexto de la tarea actual")
    parser.add_argument("--top", type=int, default=3, help="Resultados por fuente (default: 3)")
    parser.add_argument("--json", action="store_true", help="Salida JSON pura")
    parser.add_argument("--no-skills", action="store_true", help="Omitir sugerencia de skills")
    args = parser.parse_args()

    query = args.query or " ".join(sys.argv[1:]).strip()
    if not query:
        print('❌ Uso: route_memory.py "contexto de la tarea"')
        sys.exit(1)

    db_path = str(LANCEDB_DIR)
    if not Path(db_path).exists():
        print("❌ LanceDB no encontrado en", db_path)
        sys.exit(1)

    db = lancedb.connect(db_path)
    model = cargar_modelo()
    q_emb = model.encode([query], normalize_embeddings=True)[0]

    tipo = clasificar_tarea(query)

    # ── Buscar en conocimiento ──
    conocimientos = []
    try:
        tbl = db.open_table(KNOWLEDGE_TABLE)
        rows = tbl.to_pandas()
        for _, row in rows.iterrows():
            emb = row["vector"]
            if emb is None:
                continue
            # AISLAMIENTO: registros tipo 'biblioteca' (Goku-iam) solo
            # emergen cuando la tarea es de estudio/biblioteca/RAG.
            if row["tipo"] == "biblioteca" and tipo != "biblioteca":
                continue
            sim = cosine_similarity(q_emb, emb)
            conocimientos.append(
                {
                    "titulo": row["titulo"],
                    "tipo": row["tipo"],
                    "fuente": row["fuente"],
                    "peso": int(row["peso"]),
                    "similarity": round(sim, 4),
                }
            )
        conocimientos.sort(key=lambda x: x["similarity"], reverse=True)
    except Exception as e:
        print(f"  ⚠ Aviso conocimiento: {e}")

    # ── Buscar en skill_index ──
    skills = []
    if not args.no_skills:
        try:
            tbl = db.open_table(SKILL_TABLE)
            rows = tbl.to_pandas()
            for _, row in rows.iterrows():
                emb = row["embedding"]
                if emb is None:
                    continue
                sim = cosine_similarity(q_emb, emb)
                skills.append(
                    {
                        "skill_name": row["skill_name"],
                        "description": row["description"],
                        "path": row["path"],
                        "similarity": round(sim, 4),
                    }
                )
            skills.sort(key=lambda x: x["similarity"], reverse=True)
        except Exception as e:
            print(f"  ⚠ Aviso skills: {e}")

    top_skills = skills[: args.top]
    top_conocimiento = conocimientos[: args.top]

    if args.json:
        print(
            json.dumps(
                {
                    "query": query,
                    "clasificacion": tipo,
                    "skills": top_skills,
                    "conocimiento": top_conocimiento,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    print("\n🧭 ENRUTADOR SEMÁNTICO DE HERMANAIA")
    print("=" * 60)
    print(f"📌 Tarea detectada: [{tipo.upper()}]")
    print()

    if top_skills:
        print("🎯 SKILLS RELEVANTES (cargar estas herramientas):")
        for i, s in enumerate(top_skills, 1):
            pct = s["similarity"] * 100
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"  {i}. {s['skill_name']} [{bar}] {pct:.0f}%")
            print(f"     📝 {s['description'][:90]}")
        print()

    if top_conocimiento:
        print("🧠 CONOCIMIENTO PERTINENTE (recordar):")
        for i, c in enumerate(top_conocimiento, 1):
            pct = c["similarity"] * 100
            print(f"  {i}. [{c['tipo']}/{c['peso']}] {c['titulo'][:60]} ({pct:.0f}%)")
            print(f"     📌 {c['fuente']}")
        print()

    print("✅ Enrutamiento completo. Usa las skills sugeridas y el conocimiento pertinente.")


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
