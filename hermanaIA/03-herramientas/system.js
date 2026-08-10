import { execSync } from "child_process";

export default {
  description: "Query system information: CPU, RAM, disk, GPU, OS, kernel, temperature",
  args: {
    category: {
      type: "string",
      description: "Info category: 'overview' (default), 'disk', 'memory', 'cpu', 'gpu', 'processes', 'temperature', 'packages'",
    },
  },
  async execute(args) {
    const cat = args.category || "overview";
    const results = [];

    if (cat === "overview" || cat === "os") {
      results.push("--- OS ---");
      results.push(execSync("uname -a 2>/dev/null || echo unknown").toString().trim());
    }
    if (cat === "overview" || cat === "memory") {
      results.push("--- MEMORY ---");
      results.push(execSync("free -h 2>/dev/null || echo 'free not available'").toString().trim());
    }
    if (cat === "overview" || cat === "disk") {
      results.push("--- DISK ---");
      results.push(execSync("df -h / /home 2>/dev/null || df -h /").toString().trim());
    }
    if (cat === "overview" || cat === "cpu") {
      results.push("--- CPU ---");
      results.push(execSync("lscpu 2>/dev/null | grep -E 'Model name|CPU\\(s\\)|Thread|Core|Socket|MHz' || cat /proc/cpuinfo 2>/dev/null | grep -m5 'model name' || echo 'N/A'").toString().trim());
      results.push("--- LOAD ---");
      results.push(execSync("uptime 2>/dev/null").toString().trim());
    }
    if (cat === "overview" || cat === "gpu") {
      results.push("--- GPU ---");
      const nvidia = execSync("nvidia-smi --query-gpu=name,memory.total,temperature.gpu --format=csv,noheader 2>/dev/null || echo ''").toString().trim();
      results.push(nvidia || "No NVIDIA GPU found");
    }
    if (cat === "overview" || cat === "temperature") {
      results.push("--- TEMPERATURE ---");
      const temp = execSync("cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null || echo ''").toString().trim();
      results.push(temp ? temp.split("\n").map((l, i) => `Zone ${i}: ${(parseInt(l) / 1000).toFixed(1)}°C`).join("\n") : "No thermal data");
    }
    if (cat === "processes") {
      results.push("--- TOP PROCESSES ---");
      results.push(execSync("ps aux --sort=-%mem 2>/dev/null | head -15 || ps aux 2>/dev/null | head -15").toString().trim());
    }
    if (cat === "packages") {
      results.push("--- KEY PACKAGES ---");
      const pkgs = {};
      for (const [name, cmd, flag] of [["Node", "node --version", ""], ["Python", "python3 --version", ""], ["npm", "npm --version", ""], ["tsx", "tsx --version", ""], ["Git", "git --version", ""], ["Docker", "docker --version", ""], ["Rust", "rustc --version", ""], ["Go", "go version", ""]]) {
        try {
          pkgs[name] = execSync(cmd).toString().trim();
        } catch { pkgs[name] = "not installed"; }
      }
      results.push(Object.entries(pkgs).map(([k, v]) => `${k}: ${v}`).join("\n"));
    }

    return results.join("\n\n");
  },
};
