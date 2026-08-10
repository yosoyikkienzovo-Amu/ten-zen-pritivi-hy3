import { appendFileSync, mkdirSync, existsSync, readFileSync, writeFileSync } from "fs";
import { join } from "path";
import { homedir } from "os";

export default {
  description: "Save or load cross-session context notes. Persists key information across conversations.",
  args: {
    action: {
      type: "string",
      description: "'save' (default) to store a note, 'list' to show saved notes, 'read' to view a specific note",
    },
    title: { type: "string", description: "Note title (used as filename for save/read)" },
    content: { type: "string", description: "Note content to save (required for action='save')" },
    tag: { type: "string", description: "Filter by tag when listing" },
  },
  async execute(args) {
    const notesDir = join(homedir(), ".config", "opencode", "notes");
    mkdirSync(notesDir, { recursive: true });

    const action = args.action || "save";

    if (action === "save") {
      const title = args.title || `note-${Date.now()}`;
      const safeName = title.replace(/[^a-zA-Z0-9_-]/g, "_") + ".md";
      const path = join(notesDir, safeName);
      const header = `# ${title}\n> Saved: ${new Date().toISOString()}\n${args.tag ? `> Tag: ${args.tag}\n` : ""}\n`;
      writeFileSync(path, header + (args.content || ""));
      return `✅ Saved: ${path}`;
    }

    if (action === "list") {
      const files = existsSync(notesDir) ? require("fs").readdirSync(notesDir).filter(f => f.endsWith(".md")) : [];
      if (files.length === 0) return "No saved notes.";
      const list = files.map(f => {
        const firstLine = readFileSync(join(notesDir, f), "utf-8").split("\n")[0] || f;
        const tagMatch = readFileSync(join(notesDir, f), "utf-8").match(/> Tag: (.+)/);
        const tag = tagMatch ? tagMatch[1] : "";
        const matches = !args.tag || tag.includes(args.tag);
        return matches ? `- ${f.replace(".md", "")}: ${firstLine.replace("# ", "")}${tag ? ` [${tag}]` : ""}` : null;
      }).filter(Boolean);
      return list.length ? list.join("\n") : "No notes match that tag.";
    }

    if (action === "read") {
      if (!args.title) return "❌ Specify title to read.";
      const safeName = args.title.replace(/[^a-zA-Z0-9_-]/g, "_") + ".md";
      const path = join(notesDir, safeName);
      if (!existsSync(path)) return `❌ Note '${args.title}' not found.`;
      return readFileSync(path, "utf-8");
    }

    return `❌ Unknown action: ${action}. Use 'save', 'list', or 'read'.`;
  },
};
