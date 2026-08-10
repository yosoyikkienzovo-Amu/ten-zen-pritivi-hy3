# Obsidian Connections - Session 2026-05-26

## MCP Connection (obsidian-kumra)
- **URL**: http://172.19.0.1:27123
- **Token**: 8f3e3d8182af73d0b49433e34c3b5576e1eea279871934d727145a817eff6cfa
- **Config**: ~/.hermes/config.yaml under mcp_servers.obsidian-kumra
- **Status**: Configured, curl blocked in WSL - use python3 urllib.request

## claude-obsidian Vault
- **Path**: /mnt/c/ClaudeHub/MCP/claude-obsidian/
- **Skills**: 11 (wiki, wiki-ingest, wiki-query, wiki-lint, wiki-fold, save, autoresearch, canvas, defuddle, obsidian-markdown, obsidian-bases)
- **Pattern**: Karpathy's LLM Wiki

## Memory Bridge
- **Port**: 7777
- **Script**: /home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3/bridge/memory_bridge.py
- **Status**: Inactive, needs terminal(background=true) to start

## Host IP Resolution
```bash
HOST_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
```
