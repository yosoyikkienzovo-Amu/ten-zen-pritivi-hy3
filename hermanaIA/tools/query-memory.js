import { execFileSync } from "child_process";
import { join } from "path";
import { homedir } from "os";

const OPCODE_DIR = join(homedir(), ".config", "opencode");
const VENV_PY = join(OPCODE_DIR, "memoria-superior", "venv", "bin", "python3");
const QUERY_SCRIPT = join(OPCODE_DIR, "memoria-superior", "scripts", "query_lancedb.py");

export default {
  description:
    "Busqueda semantica en la memoria vectorial de hermanaIA (LanceDB). Consulta conocimientos, conquistas, directivas y progreso indexados. Uso: query-memory <consulta>",
  args: {
    query: {
      type: "string",
      description: "Texto de busqueda semantica (ej. 'que es la memoria superior')",
    },
    limit: {
      type: "number",
      description: "Numero de resultados (defecto: 5)",
    },
    tipo: {
      type: "string",
      description: "Filtrar por tipo: directiva, conquista, memoria_trabajo, progreso, sugerencia, tarea",
    },
    minPeso: {
      type: "number",
      description: "Peso minimo (1-10)",
    },
    raw: {
      type: "boolean",
      description: "Salida JSON cruda (para parsear programaticamente)",
    },
  },
  async execute(args) {
    if (!args.query) {
      return "Uso: query-memory <consulta> [--limit N] [--tipo X] [--minPeso N] [--raw true]";
    }

    const cmdArgs = [QUERY_SCRIPT, args.query];
    if (args.limit) cmdArgs.push("--limit", String(args.limit));
    if (args.tipo) cmdArgs.push("--tipo", args.tipo);
    if (args.minPeso) cmdArgs.push("--min-peso", String(args.minPeso));
    if (args.raw) cmdArgs.push("--raw");

    try {
      const out = execFileSync(VENV_PY, cmdArgs, {
        encoding: "utf8",
        timeout: 120000,
        env: { ...process.env, HF_HUB_OFFLINE: "0" },
      });
      return out.trim() || "Sin resultados.";
    } catch (err) {
      return `Error en query-memory: ${err.stderr || err.message}`;
    }
  },
};
