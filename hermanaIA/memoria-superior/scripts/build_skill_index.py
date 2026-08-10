#!/usr/bin/env python3
import sys
import yaml
import lancedb
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from model_utils import cargar_modelo

SKILLS_DIR = Path.home() / ".config" / "opencode" / "skills"
LANCEDB_DIR = Path.home() / ".config" / "opencode" / "memoria-superior" / "lancedb"
TABLE_NAME = "skill_index"

def extract_frontmatter(text: str) -> dict:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                return yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                pass
    return {}

def main():
    print("🔍 Escaneando skills...")
    skills = []
    for entry in sorted(SKILLS_DIR.iterdir()):
        if not entry.is_dir():
            continue
        sk_file = entry / "SKILL.md"
        if not sk_file.exists():
            continue
        text = sk_file.read_text(encoding="utf-8", errors="ignore")
        meta = extract_frontmatter(text)
        name = meta.get("name", entry.name)
        description = meta.get("description", "")
        if not description:
            for line in text.splitlines():
                s = line.strip()
                if s and not s.startswith("#") and not s.startswith("---"):
                    description = s[:200]
                    break
        skills.append({"name": name, "description": description, "path": str(sk_file)})

    if not skills:
        print("❌ No se encontraron skills con SKILL.md")
        sys.exit(1)

    print(f"📦 {len(skills)} skills encontradas. Generando embeddings...")

    model = cargar_modelo()
    texts = [s["description"] for s in skills]
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    print(f"💾 Conectando a LanceDB en {LANCEDB_DIR}...")
    LANCEDB_DIR.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(str(LANCEDB_DIR))

    if TABLE_NAME in db.table_names():
        db.drop_table(TABLE_NAME)
        print("  ↺ Tabla existente eliminada")

    data = []
    for s, emb in zip(skills, embeddings):
        data.append({
            "skill_name": s["name"],
            "description": s["description"],
            "path": s["path"],
            "embedding": emb.tolist(),
        })

    tbl = db.create_table(TABLE_NAME, data)
    print(f"✅ Índice creado: {len(data)} skills en tabla '{TABLE_NAME}'")
    print(f"📍 Ubicación: {LANCEDB_DIR / TABLE_NAME}")

if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
