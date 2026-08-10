#!/usr/bin/env python3
import os
import re
import yaml
from pathlib import Path

SKILLS_DIR = Path.home() / ".config" / "opencode" / "skills"

def extract_description_from_md(text: str) -> str | None:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                data = yaml.safe_load(parts[1])
                if isinstance(data, dict):
                    desc = data.get("description") or data.get("Descripción") or data.get("descripción")
                    if desc and isinstance(desc, str):
                        return desc.strip()
            except yaml.YAMLError:
                pass
    for line in text.splitlines():
        s = line.strip()
        if s and not s.startswith("#") and not s.startswith("!"):
            return s[:200]
    return None

def extract_name_from_dir(dirname: str) -> str:
    name = dirname.lower().strip()
    name = re.sub(r'[_\s]+', '-', name)
    name = re.sub(r'[^a-z0-9-]', '', name)
    name = re.sub(r'-+', '-', name).strip('-')
    return name if name else dirname

def main():
    converted = 0
    skipped = 0
    errors = 0

    for entry in sorted(SKILLS_DIR.iterdir()):
        if not entry.is_dir():
            continue
        sk_file = entry / "SKILL.md"
        if sk_file.exists():
            skipped += 1
            continue

        name = extract_name_from_dir(entry.name)
        description = None

        desc_file = entry / "DESCRIPTION.md"
        if desc_file.exists():
            text = desc_file.read_text(encoding="utf-8", errors="ignore")
            description = extract_description_from_md(text)

        if not description:
            for f in sorted(entry.iterdir()):
                if f.suffix == ".md" and f.name != "DESCRIPTION.md" and f.name != "SKILL.md":
                    text = f.read_text(encoding="utf-8", errors="ignore")
                    description = extract_description_from_md(text)
                    if description:
                        break

        if not description:
            first_file = next((f for f in sorted(entry.iterdir()) if f.is_file()), None)
            if first_file:
                text = first_file.read_text(encoding="utf-8", errors="ignore")
                description = extract_description_from_md(text)

        if not description:
            description = f"Skill: {entry.name}"

        content = f"---\nname: {name}\ndescription: {description}\n---\n\n# {entry.name}\n\n{description}\n"
        try:
            sk_file.write_text(content, encoding="utf-8")
            print(f"  ✅ CREADO: {entry.name}/SKILL.md ← '{description[:60]}...'")
            converted += 1
        except Exception as e:
            print(f"  ❌ ERROR: {entry.name} → {e}")
            errors += 1

    print(f"\nResumen: {converted} creados, {skipped} ya existían, {errors} errores")

if __name__ == "__main__":
    main()
