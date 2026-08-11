import { execFileSync } from "child_process";
import { join } from "path";
import { homedir } from "os";

const OPCODE_DIR = join(homedir(), ".config", "opencode");
const VENV_PY = join(OPCODE_DIR, "memoria-superior", "venv", "bin", "python3");
const ROUTE_SCRIPT = join(OPCODE_DIR, "memoria-superior", "scripts", "route_memory.py");

export default {
  description:
    "Enrutador semantico automatico de hermanaIA. Dado el contexto de la tarea actual, clasifica su tipo y sugiere las skills y el conocimiento mas relevantes de la memoria vectorial. Uso: route-memory <contexto de la tarea>",
  args: {
    query: {
      type: "string",
      description: "Contexto o descripcion de la tarea actual (ej. 'voy a automatizar un backup con cron')",
    },
    top: {
      type: "number",
      description: "Resultados por fuente (defecto: 3)",
    },
    noSkills: {
      type: "boolean",
      description: "Omitir sugerencia de skills (solo conocimiento)",
    },
    raw: {
      type: "boolean",
      description: "Salida JSON cruda (para parsear programaticamente)",
    },
  },
  async execute(args) {
    if (!args.query) {
      return "Uso: route-memory <contexto de la tarea> [--top N] [--noSkills true] [--raw true]";
    }

    const cmdArgs = [ROUTE_SCRIPT, args.query];
    if (args.top) cmdArgs.push("--top", String(args.top));
    if (args.noSkills) cmdArgs.push("--no-skills");
    if (args.raw) cmdArgs.push("--json");

    try {
      const out = execFileSync(VENV_PY, cmdArgs, {
        encoding: "utf8",
        timeout: 120000,
        env: { ...process.env, HF_HUB_OFFLINE: "0" },
      });
      return out.trim() || "Sin resultados.";
    } catch (err) {
      return `Error en route-memory: ${err.stderr || err.message}`;
    }
  },
};
