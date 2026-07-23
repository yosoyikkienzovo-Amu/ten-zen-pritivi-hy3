#!/usr/bin/env python3
# ingest_to_lancedb.py
# Ingesta de archivos del sistema en memoria vectorial LanceDB
# Uso: python3 scripts/ingest_to_lancedb.py [--force]
# --force: recrea la tabla desde cero

import lancedb
import uuid
import sys
import re
import os
from pathlib import Path
from datetime import datetime
from model_utils import cargar_modelo, MODEL_NAME, CACHE_DIR

HOME = Path.home()
BASE = HOME / ".config/opencode"
DB_DIR = BASE / "memoria-superior" / "lancedb"
CACHE_DIR = BASE / "memoria-superior" / "embeddings"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

SEGMENTOS = []

def seg(archivo_rel, contenido, tipo_por_defecto="general", peso_defecto=5):
    SEGMENTOS.append({
        "archivo": archivo_rel,
        "contenido": contenido,
        "tipo": tipo_por_defecto,
        "peso": peso_defecto,
    })

def segmentar_agentes_md():
    path = BASE / "AGENTS.md"
    if not path.exists(): return
    raw = path.read_text(encoding="utf-8")
    titulo_actual = None
    lineas = []
    for line in raw.split("\n"):
        if line.startswith("#") and not line.startswith("##"):
            if titulo_actual and lineas:
                c = "\n".join(lineas).strip()
                if c:
                    seg("AGENTS.md", f"{titulo_actual}\n{c}", "directiva", 10)
            titulo_actual = line.lstrip("# ").strip()
            lineas = []
        else:
            lineas.append(line)
    if titulo_actual and lineas:
        c = "\n".join(lineas).strip()
        if c:
            seg("AGENTS.md", f"{titulo_actual}\n{c}", "directiva", 10)

def segmentar_memory_md():
    path = BASE / "MEMORY.md"
    if not path.exists(): return
    raw = path.read_text(encoding="utf-8")
    secciones = re.split(r"\n## ", raw)
    for s in secciones:
        if not s.strip(): continue
        lines = s.strip().split("\n")
        titulo = lines[0].strip().lstrip("#").strip()
        contenido = "\n".join(lines[1:]).strip()
        if contenido:
            seg("MEMORY.md", f"{titulo}\n{contenido}", "memoria_trabajo", 7)

def segmentar_cumplidas_txt():
    path = BASE / "conquistas" / "cumplidas.txt"
    if not path.exists(): return
    raw = path.read_text(encoding="utf-8")
    for line in raw.split("\n"):
        line = line.strip()
        if not line: continue
        m = re.match(r"^\[(\d{4}-\d{2}-\d{2})", line)
        if m:
            seg("cumplidas.txt", line, "conquista", 6)

def segmentar_progreso_md():
    path = BASE / "conquistas" / "progreso.md"
    if not path.exists(): return
    raw = path.read_text(encoding="utf-8")
    secciones = re.split(r"\n### ", raw)
    for s in secciones:
        if not s.strip(): continue
        lines = s.strip().split("\n")
        titulo = lines[0].strip().lstrip("#").strip()
        contenido = "\n".join(lines[1:]).strip()
        if contenido and titulo:
            seg("progreso.md", f"{titulo}\n{contenido}", "progreso", 5)

def segmentar_sugerencias_md():
    path = BASE / "conquistas" / "sugerencias-sistema.md"
    if not path.exists(): return
    raw = path.read_text(encoding="utf-8")
    seg("sugerencias-sistema.md", raw, "sugerencia", 7)

def segmentar_pendientes_txt():
    path = BASE / "conquistas" / "pendientes.txt"
    if not path.exists(): return
    raw = path.read_text(encoding="utf-8")
    for line in raw.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"): continue
        seg("pendientes.txt", line, "tarea", 8)

def segmentar_md_intercambios():
    dir_path = BASE / "intercambios"
    if not dir_path.exists(): return
    for path in sorted(dir_path.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        secciones = re.split(r"\n## ", raw)
        for s in secciones:
            if not s.strip(): continue
            lines = s.strip().split("\n")
            titulo = lines[0].strip().lstrip("#").strip()
            contenido = "\n".join(lines[1:]).strip()
            if contenido:
                seg(f"intercambios/{path.name}", f"{titulo}\n{contenido}", "intercambio", 6)

def segmentar_spec_root():
    path = BASE / "hermanaIA.spec.md"
    if not path.exists(): return
    raw = path.read_text(encoding="utf-8")
    secciones = re.split(r"\n## ", raw)
    for s in secciones:
        if not s.strip(): continue
        lines = s.strip().split("\n")
        titulo = lines[0].strip().lstrip("#").strip()
        contenido = "\n".join(lines[1:]).strip()
        if contenido:
            seg("hermanaIA.spec.md", f"{titulo}\n{contenido}", "spec", 8)

def inferir_tags(contenido, tipo):
    tags = [tipo]
    if "respiracion" in contenido.lower() or "respirar" in contenido.lower():
        tags.append("respiracion")
    if "seguridad" in contenido.lower() or "backup" in contenido.lower():
        tags.append("seguridad")
    if "directriz" in contenido.lower() or "directiva" in contenido.lower() or "maestra" in contenido.lower():
        tags.append("directriz")
    if "palacio" in contenido.lower() or "habitacion" in contenido.lower():
        tags.append("palacio")
    if "lancedb" in contenido.lower() or "vectorial" in contenido.lower():
        tags.append("vectorial")
    if "observ" in contenido.lower() or "vault" in contenido.lower():
        tags.append("obsidian")
    if "make" in contenido.lower() or "comando" in contenido.lower():
        tags.append("comando")
    if "puente" in contenido.lower() or "intercambio" in contenido.lower() or "externo" in contenido.lower():
        tags.append("puente")
    if "handoff" in contenido.lower() or "spec" in contenido.lower() or "multi-agente" in contenido.lower():
        tags.append("coordinacion")
    return list(set(tags))

def main():
    force = "--force" in sys.argv

    print("Cargando modelo de embeddings...")
    model = cargar_modelo()

    print("Segmentando archivos del sistema...")
    segmentar_agentes_md()
    segmentar_memory_md()
    segmentar_cumplidas_txt()
    segmentar_progreso_md()
    segmentar_sugerencias_md()
    segmentar_pendientes_txt()
    segmentar_md_intercambios()
    segmentar_spec_root()

    print(f"Total segmentos: {len(SEGMENTOS)}")

    db = lancedb.connect(str(DB_DIR))

    if "conocimiento" in db.list_tables().tables:
        db.drop_table("conocimiento")

    tabla = db.create_table("conocimiento", [
        {
            "id": str(uuid.uuid4())[:8],
            "tipo": s["tipo"],
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "titulo": s["contenido"][:80].split("\n")[0],
            "contenido": s["contenido"][:2000],
            "fuente": s["archivo"],
            "tags": inferir_tags(s["contenido"], s["tipo"]),
            "peso": s["peso"],
            "vector": model.encode(s["contenido"][:2000]).tolist(),
        }
        for s in SEGMENTOS
    ])
    print(f"Tabla 'conocimiento' creada con {len(tabla)} registros")

    # Mostrar distribución
    dist = {}
    for s in SEGMENTOS:
        dist[s["archivo"]] = dist.get(s["archivo"], 0) + 1
    print("\n--- Distribucion por archivo ---")
    for arch, count in sorted(dist.items()):
        print(f"  {arch}: {count} segmentos")

if __name__ == "__main__":
    main()
