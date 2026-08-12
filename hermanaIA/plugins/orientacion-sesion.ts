import { readFileSync, existsSync } from "node:fs"
import { execFile } from "node:child_process"
import type { PluginModule } from "@opencode-ai/plugin"

const MEMORY = "/home/ikki/.config/opencode/MEMORY.md"
const SCRIPT = "/home/ikki/.config/opencode/conquistas/orientacion-diaria.sh"

const seen = new Set<string>()

function today(): string {
  return new Date().toISOString().slice(0, 10)
}

function extractPriority(content: string): string | null {
  const m = content.match(/## ORIENTACIÓN DEL DÍA \(\d{4}-\d{2}-\d{2} (\d{2}:\d{2})\)([\s\S]*?)(?=^## |\z)/m)
  if (!m) return null
  const block = m[2]
  const p = block.match(/PRIORIDAD DEL DÍA[^\n]*\n\s*([^\n]+)/)
  return p ? p[1].trim() : null
}

export default {
  id: "local.orientacion-sesion",
  async server(input) {
    return {
      async event({ event }) {
        if (event.type !== "session.created") return
        const sid = (event as any).properties?.info?.id as string | undefined
        if (!sid || seen.has(sid)) return
        seen.add(sid)

        const todayStr = today()
        let content = ""
        if (existsSync(MEMORY)) content = readFileSync(MEMORY, "utf8")
        const hasToday = new RegExp(`## ORIENTACIÓN DEL DÍA \\(${todayStr} `).test(content)

        if (!hasToday) {
          execFile("bash", [SCRIPT], { timeout: 90000 }, (_err) => {
            if (existsSync(MEMORY)) content = readFileSync(MEMORY, "utf8")
            const prio = extractPriority(content)
            input.client.showToast({
              title: "Orientación del día",
              message: prio ? `🎯 ${prio}` : "Sin pendientes pesadas",
              variant: "success",
              duration: 6000,
            })
          })
          return
        }

        const prio = extractPriority(content)
        input.client.showToast({
          title: "Orientación del día",
          message: prio ? `🎯 ${prio}` : "Sin pendientes pesadas",
          variant: "success",
          duration: 6000,
        })
      },
    }
  },
} satisfies PluginModule
