---
name: deepwiki
description: "DeepWiki MCP provides AI-powered documentation for GitHub repositories.\n\nAvailable tools:\n- read_wiki_structure: Get a list of documentation topics for a repository\n- read_wiki_contents: View full documentation about a repository\n- ask_question: Ask any question about a repository and get an AI-powered answer\n- list_available_repos: List your available repositories (private mode only)\n- generate_wiki: Generate a codebase wiki for a repository — only use when explicitly requested by the user (private mode only)\n- devin_knowledge_manage: Manage Devin knowledge notes and suggestions — list, search, get, create, update, delete notes, view folder structure, list/view/dismiss knowledge suggestions (private mode only)\n- devin_playbook_manage: Manage Devin playbooks — list, get, create, update, delete (private mode only)\n- devin_schedule_manage: Manage scheduled Devin sessions — list, get, create, update, delete (private mode only)\n- devin_session_create: Create one or more child Devin sessions (private mode only)\n- devin_session_interact: Manage a Devin session — get status, send messages, sleep/terminate/archive, read messages & attachments, manage tags (private mode only)\n- devin_session_events: Inspect session events — list summaries, fetch full details, or search event contents (private mode only)\n- devin_session_search: Search and filter Devin sessions (private mode only)\n- list_integrations: List all native integrations and MCP servers with their status and settings URLs (private mode only)\n Triggers on: read_wiki_structure, read_wiki_contents, ask_question."
version: 1.0.0
author: mcptoskill
license: MIT
metadata: {"hermes":{"tags":["read_wiki_structure","read_wiki_contents","ask_question"],"category":"mcptoskill"}}
---

# DeepWiki

DeepWiki MCP provides AI-powered documentation for GitHub repositories.

Available tools:
- read_wiki_structure: Get a list of documentation topics for a repository
- read_wiki_contents: View full documentation about a repository
- ask_question: Ask any question about a repository and get an AI-powered answer
- list_available_repos: List your available repositories (private mode only)
- generate_wiki: Generate a codebase wiki for a repository — only use when explicitly requested by the user (private mode only)
- devin_knowledge_manage: Manage Devin knowledge notes and suggestions — list, search, get, create, update, delete notes, view folder structure, list/view/dismiss knowledge suggestions (private mode only)
- devin_playbook_manage: Manage Devin playbooks — list, get, create, update, delete (private mode only)
- devin_schedule_manage: Manage scheduled Devin sessions — list, get, create, update, delete (private mode only)
- devin_session_create: Create one or more child Devin sessions (private mode only)
- devin_session_interact: Manage a Devin session — get status, send messages, sleep/terminate/archive, read messages & attachments, manage tags (private mode only)
- devin_session_events: Inspect session events — list summaries, fetch full details, or search event contents (private mode only)
- devin_session_search: Search and filter Devin sessions (private mode only)
- list_integrations: List all native integrations and MCP servers with their status and settings URLs (private mode only)


## Quick Start

```bash
$HOME/.hermes/skills/mcptoskill/deepwiki/scripts/deepwiki.sh <tool-name> '<json-args>'
```

## Tools

### read_wiki_structure

Get a list of documentation topics for a GitHub repository.

Args:
    repoName: GitHub repository in owner/repo format (e.g. "facebook/react")

**Parameters:**
  - `repoName` (string) (required)

```bash
$HOME/.hermes/skills/mcptoskill/deepwiki/scripts/deepwiki.sh read_wiki_structure '{"repoName":"<repoName>"}'
```

### read_wiki_contents

View documentation about a GitHub repository.

Args:
    repoName: GitHub repository in owner/repo format (e.g. "facebook/react")

**Parameters:**
  - `repoName` (string) (required)

```bash
$HOME/.hermes/skills/mcptoskill/deepwiki/scripts/deepwiki.sh read_wiki_contents '{"repoName":"<repoName>"}'
```

### ask_question

Ask any question about a GitHub repository and get an AI-powered, context-grounded response.

Args:
    repoName: GitHub repository or list of repositories (max 10) in owner/repo format
    question: The question to ask about the repository

**Parameters:**
  - `repoName` (string) (required)
  - `question` (string) (required)

```bash
$HOME/.hermes/skills/mcptoskill/deepwiki/scripts/deepwiki.sh ask_question '{"repoName":"<repoName>","question":"<question>"}'
```
