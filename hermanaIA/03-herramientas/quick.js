import { execSync } from "child_process";
import { readFileSync, readdirSync, existsSync } from "fs";
import { join } from "path";
import { homedir } from "os";

export default {
  description: "Quick actions: run system commands, search skills, manage sessions, get shortcuts for common workflows",
  args: {
    action: {
      type: "string",
      description: "Action: 'skills' (list available), 'opencode-status', 'session-save' (save current session log), 'shortcuts' (show useful keybinds)",
    },
  },
  async execute(args) {
    const act = args.action || "shortcuts";

    if (act === "skills") {
      const skillsDir = join(homedir(), ".config", "opencode", "skills");
      if (!existsSync(skillsDir)) return "No skills directory found.";
      const cats = readdirSync(skillsDir, { withFileTypes: true }).filter(d => d.isDirectory());
      const lines = ["--- AVAILABLE SKILLS ---"];
      for (const cat of cats) {
        const skills = readdirSync(join(skillsDir, cat.name)).filter(s => s.endsWith(".md") || existsSync(join(skillsDir, cat.name, s, "SKILL.md")));
        if (skills.length) lines.push(`\n${cat.name}/`);
        for (const s of skills) {
          const skillPath = existsSync(join(skillsDir, cat.name, s, "SKILL.md"))
            ? join(skillsDir, cat.name, s, "SKILL.md") : join(skillsDir, cat.name, s);
          const firstLine = readFileSync(skillPath, "utf-8").split("\n")[0] || s;
          lines.push(`  - ${s.replace(".md", "")}: ${firstLine.replace(/^#\s*/, "")}`);
        }
      }
      return lines.join("\n");
    }

    if (act === "opencode-status") {
      const config = readFileSync(join(homedir(), ".config", "opencode", "opencode.json"), "utf-8");
      const parsed = JSON.parse(config);
      const parts = [
        `Model: ${parsed.model}`,
        `LSP: ${parsed.lsp ? "enabled" : "disabled"}`,
        `MCPs: ${Object.keys(parsed.mcp || {}).join(", ") || "none"}`,
        `References: ${Object.keys(parsed.references || {}).join(", ") || "none"}`,
        `Commands: ${Object.keys(parsed.command || {}).length || 0}`,
        `Agents: ${Object.keys(parsed.agent || {}).length || 0}`,
      ];
      return ["--- OPENCODE STATUS ---", ...parts].join("\n");
    }

    if (act === "shortcuts") {
      return [
        "--- SHORTCUTS ---",
        "/plan        Create an implementation plan",
        "/spec        Write a specification",
        "/review      Review recent changes",
        "/test        Generate/run tests",
        "/deploy      Build and package",
        "/simplify    Simplify recent code",
        "",
        "MCP tools:",
        "  context7  → documentation for any library",
        "  websearch → search the web",
        "  gh_grep   → search code on GitHub",
        "",
        "Custom tools:",
        "  system   → query system info",
        "  context-save → save/load notes across sessions",
        "  quick    → skills list, status, shortcuts",
      ].join("\n");
    }

    return `❌ Unknown action: ${act}`;
  },
};
