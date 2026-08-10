import { execFileSync } from "child_process";
import { join } from "path";
import { homedir } from "os";

const OPCODE_DIR = join(homedir(), ".config", "opencode");
const VENV_PY = join(OPCODE_DIR, "memoria-superior", "venv", "bin", "python3");
const ADD_SCRIPT = join(OPCODE_DIR, "memoria-superior", "scripts", "add_to_memory.py");

export default {
  description:
    "Guarda un registro en la memoria vectorial de hermanaIA (LanceDB). Para persistir conocimiento, aprendizajes o reflexiones. Uso: save-memory <titulo> <contenido>",
  args: {
    titulo: {
      type: "string",
      description: "Titulo corto del registro (max 80 chars)",
    },
    contenido: {
      type: "string",
      description: "Contenido del registro (max 2000 chars)",
    },
    tipo: {
      type: "string",
      description: "Tipo: directiva, conquista, memoria_trabajo, progreso, sugerencia, tarea, spec, intercambio, reflexion (defecto: memoria_trabajo)",
    },
    fuente: {
      type: "string",
      description: "Origen del registro (defecto: opencode-tool)",
    },
    peso: {
      type: "number",
      description: "Importancia 1-10 (defecto: 6)",
    },
    tags: {
      type: "string",
      description: "Tags extra separadas por coma",
    },
  },
  async execute(args) {
    if (!args.titulo || !args.contenido) {
      return "Uso: save-memory <titulo> <contenido> [--tipo X] [--fuente Y] [--peso N] [--tags a,b,c]";
    }

    const cmdArgs = [ADD_SCRIPT, "--titulo", args.titulo, "--contenido", args.contenido];
    if (args.tipo) cmdArgs.push("--tipo", args.tipo);
    if (args.fuente) cmdArgs.push("--fuente", args.fuente);
    if (args.peso) cmdArgs.push("--peso", String(args.peso));
    if (args.tags) cmdArgs.push("--tags", args.tags);

    try {
      const out = execFileSync(VENV_PY, cmdArgs, {
        encoding: "utf8",
        timeout: 120000,
        env: { ...process.env, HF_HUB_OFFLINE: "0" },
      });
      return out.trim();
    } catch (err) {
      return `Error en save-memory: ${err.stderr || err.message}`;
    }
  },
};
