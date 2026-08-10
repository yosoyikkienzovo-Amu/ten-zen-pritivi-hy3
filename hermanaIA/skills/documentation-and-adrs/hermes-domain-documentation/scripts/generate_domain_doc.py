import os, subprocess, json, datetime, pathlib, sys
from pathlib import Path

def sh(cmd_list):
    """Run command without shell for safety."""
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True, timeout=10)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", 1

base = Path.home() / '.hermes'
output_dir = base / 'outputs' / 'domain_doc'
output_dir.mkdir(parents=True, exist_ok=True)

# 1. Telemetry
uname_out, _, _ = sh('uname -a')
cpuinfo_out, _, _ = sh('lscpu')
mem_out, _, _ = sh('free -h')
du_out, _, _ = sh(f'du -sh {base}')
df_out, _, _ = sh('df -h -T')
hermes_ver_out, _, _ = sh('hermes --version 2>/dev/null || echo "hermes CLI not found or no version"')
env_vars = {}
for k in ['HERMES_HOME', 'PATH', 'HOME', 'USER', 'LANG', 'SHELL', 'DISPLAY', 'DBUS_SESSION_BUS_ADDRESS']:
    env_vars[k] = os.environ.get(k, '(not set)')
svc_out, _, _ = sh('systemctl list-units --type=service --state=running --no-legend 2>/dev/null || echo "systemctl not available or no services"')
timer_out, _, _ = sh('systemctl list-timers --all 2>/dev/null || echo "systemctl not available"')
uptime_out, _, _ = sh('uptime -p')

# 2. Directory sizes and tree
def get_dir_sizes(path):
    sizes = {}
    for root, dirs, files in os.walk(path):
        du_out, _, _ = sh(f'du -sh "{root}" 2>/dev/null')
        size = du_out.split()[0] if du_out else '0'
        rel = os.path.relpath(root, base)
        if rel == '.':
            rel = './'
        sizes[rel] = size
    return sizes

sizes = get_dir_sizes(base)

def tree_dir(path, prefix='', is_last=True):
    lines = []
    contents = list(path.iterdir())
    contents.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
    pointers = ['├── ', '└── ']
    for i, entry in enumerate(contents):
        is_last = i == len(contents) - 1
        line = prefix + (pointers[1] if is_last else pointers[0]) + entry.name
        lines.append(line)
        if entry.is_dir():
            extension = '    ' if is_last else '│   '
            lines.extend(tree_dir(entry, prefix + extension, is_last))
    return lines

tree_lines = tree_dir(base)
tree_text = '\n'.join(tree_lines)

# 3. Write map file
map_path = output_dir / 'hermes_domain_map.md'
with open(map_path, 'w', encoding='utf-8') as f:
    f.write('# Hermes Domain Map\n\n')
    f.write(f'Generated: {datetime.datetime.now().isoformat()}\n\n')
    f.write('## System Overview\n')
    f.write(f'- OS: {uname_out}\n')
    cpu_line = cpuinfo_out.split('\n')[0] if cpuinfo_out else 'N/A'
    f.write(f'- CPU: {cpu_line}\n')
    f.write(f'- Memory: {mem_out}\n')
    f.write(f'- Disk Usage of .hermes: {du_out}\n')
    f.write('\n## Directory Sizes\n')
    for rel, sz in sorted(sizes.items()):
        f.write(f'- `{rel}`: {sz}\n')
    f.write('\n## Directory Tree\n')
    f.write('```\n')
    f.write(tree_text)
    f.write('\n```\n')

# 4. Write documentation file
doc_path = output_dir / 'hermes_domain_documentation.md'
with open(doc_path, 'w', encoding='utf-8') as f:
    f.write('# Hermes Domain Documentation\n\n')
    f.write(f'Generated: {datetime.datetime.now().isoformat()}\n\n')
    f.write('## Environment Variables\n')
    for k, v in env_vars.items():
        f.write(f'- `{k}`: {v}\n')
    f.write('\n## Active Services (systemd)\n')
    f.write('```\n')
    f.write(svc_out if svc_out else 'None')
    f.write('\n```\n')
    f.write('\n## Timers\n')
    f.write('```\n')
    f.write(timer_out if timer_out else 'None')
    f.write('\n```\n')
    f.write('\n## Uptime\n')
    f.write(f'{uptime_out}\n\n')
    f.write('## Hermes Version\n')
    f.write(f'{hermes_ver_out}\n\n')
    f.write('## Directory & File Descriptions\n')
    doc_map = {
        'audio_cache': 'Cache for TTS audio files',
        'bin': 'Executable scripts and binaries',
        'cache': 'General cache directory',
        'conquistas': 'Achievements / logs of completed tasks',
        'cron': 'Scheduled cron job definitions',
        'data': 'General data storage',
        'gateway': 'Messaging gateway configuration and plugins',
        'hermes-agent': 'Hermes agent source code (if present)',
        'memoria_superior': 'Superior memory system (LanceDB, Obsidian vault, scripts)',
        'scripts': 'User and system scripts',
        'state-snapshots': 'Periodic snapshots of agent state',
        'skills': 'Installed skills (functionalities)',
        'AGENTS.md': 'Development guide for Hermes agent',
        'MEMORY.md': 'Persistent memory facts',
        'SOUL.md': 'Soul file (personality/identity)',
        'config.yaml': 'Main configuration file',
        'state.db': 'SQLite database for agent state',
        'lcm.db': 'LCM (Long-term Context Memory) database',
        'kanban.db': 'Kanban task database',
    }
    for entry in sorted(base.iterdir(), key=lambda x: x.name.lower()):
        name = entry.name
        rel = f'./{name}'
        desc = doc_map.get(name, 'No description available; inspect content.')
        size = sizes.get(rel, '?')
        f.write(f'### `{name}`\n')
        f.write(f'- Size: {size}\n')
        f.write(f'- Description: {desc}\n')
        f.write('\n')

# 5. Write cleanup plan
cleanup_path = output_dir / 'hermes_domain_cleanup_plan.md'
with open(cleanup_path, 'w', encoding='utf-8') as f:
    f.write('# Hermes Domain Cleanup Plan\n\n')
    f.write(f'Generated: {datetime.datetime.now().isoformat()}\n\n')
    f.write('## Recommendations\n')
    f.write('1. Review large directories (`cache`, `state-snapshots`, `audio_cache`) for stale content.\n')
    f.write('2. Check for duplicate skill or plugin versions.\n')
    f.write('3. Ensure backups of `state.db`, `lcm.db`, `kanban.db` are recent.\n')
    f.write('4. Review `config.yaml` backups; consider removing old backups after verification.\n')
    f.write('5. Verify that `hermes-agent/` source matches installed version (if using pip install).\n')
    f.write('6. Consider archiving old logs in `conquistas/` beyond a certain age.\n')
    f.write('\n## Notes\n')
    f.write('- Always backup before deletion.\n')
    f.write('- Consult skill `hermes-domain-documentation` for detailed precautions.\n')

print(f'Files written to {output_dir}')