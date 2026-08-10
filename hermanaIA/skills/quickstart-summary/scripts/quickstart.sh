#!/usr/bin/env bash
set -euo pipefail

# Determine repository root
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || REPO_ROOT="."

# Create quickstart-summary folder
mkdir -p "$REPO_ROOT/quickstart-summary"
cd "$REPO_ROOT/quickstart-summary"

# Create README.md
cat > README.md <<'EOF'
# Quickstart Summary

This repository now contains a quickstart summary for Hermes Agent, based on the official documentation at https://hermes-agent.nousresearch.com/docs/getting-started/quickstart.

## Key Steps

1. **Install Hermes Desktop** (macOS/Windows) – recommended.
2. Run `hermes setup` to:
   - Choose a provider (OpenAI, Anthropic, local, etc.).
   - Select/install a model and verify its context length.
   - Save the configuration.
3. Test with `hermes chat` (or the provided command) to ensure a working conversation.

## Configuration Tips

- **Provider selection**: pick one that fits your budget and hardware.
- **Model choice**: install the model and verify context length (e.g., 8k tokens).
- **Gateway/Bot**: use `hermes gateway setup` and connect Telegram, Discord, Slack, etc., for always‑on usage.
- **Cron jobs**: create scheduled tasks with `cronjob create …` for automation.
- **Skills**: install or write skills (`hermes skill install …`) to extend functionality.
- **Multi‑provider fallback**: configure fallback models to avoid downtime.
- **Updates & health checks**: run `hermes update` and `hermes doctor` regularly.

## Fastest Path (per documentation)

| Goal | First step | Next step |
|------|------------|-----------|
| I just want Hermes working | `hermes setup` | Run a real chat and verify response |
| I already know my provider | `hermes model` (install) | Save config, then start chatting |
| I want a bot/always‑on | `hermes gateway setup` (after CLI works) | Connect Telegram/Discord/Slack |
| I want a local/self‑hosted model | `hermes model → custom endpoint` | Verify endpoint, model name, context length |
| I want multi‑provider fallback | `hermes model first` | Add routing and fallback after base chat works |

## Why This Matters

Following the “fastest path” ensures a clean, functional chat before adding extra features, reducing troubleshooting time and increasing reliability.

--- 

*Generated from the Hermes Agent Quickstart documentation (July 2026).*
EOF

# Stage and commit changes
git add README.md
git commit -m "Add quickstart-summary README"

# Optional: push (user may need to configure upstream)
# git push origin main