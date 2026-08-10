import { readFileSync, existsSync } from "fs"
import { join } from "path"

export default {
  description: "Detecta si el proyecto actual tiene config de linter (eslint, ruff, prettier) y sugiere activación",
  args: {
    type: "object",
    properties: {
      path: {
        type: "string",
        default: ".",
        description: "Ruta del proyecto a analizar"
      }
    }
  },
  execute: async ({ path }) => {
    const cwd = path || "."
    const eslintConfigs = [
      "eslint.config.js", "eslint.config.mjs", "eslint.config.cjs",
      ".eslintrc", ".eslintrc.js", ".eslintrc.json", ".eslintrc.yaml"
    ]
    const results = { eslint: null, prettier: null, ruff: null }

    for (const cfg of eslintConfigs) {
      if (existsSync(join(cwd, cfg))) {
        results.eslint = { found: cfg, lsp_ready: true, note: "Activar con LSP en opencode.json (ya configurado)" }
        break
      }
    }

    if (existsSync(join(cwd, ".prettierrc")) || existsSync(join(cwd, ".prettierrc.json"))) {
      results.prettier = { found: true, formatter_ready: true }
    }

    if (existsSync(join(cwd, "ruff.toml")) || existsSync(join(cwd, ".ruff.toml"))) {
      results.ruff = { found: true, formatter_ready: true }
    }

    const suggestions = []
    if (results.eslint) suggestions.push("🔍 eslint config detectado — LSP listo para activarse")
    if (!results.eslint) suggestions.push("📦 Sin eslint config — si es proyecto JS/TS, considera crear eslint.config.js")
    if (!results.prettier) suggestions.push("🎨 Sin prettier config — opencode ya lo tiene como formatter global")
    if (!results.ruff) suggestions.push("🐍 Sin ruff config — opencode ya lo tiene como formatter global")

    return {
      ok: true,
      project: cwd,
      tools: results,
      suggestions: suggestions.join("\n")
    }
  }
}
