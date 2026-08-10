---
name: hooks
description: "Lifecycle hooks system: sdd-cache (HTTP cache for WebFetch with ETag revalidation) and simplify-ignore (code block protection during refactoring). Use when setting up pre/post tool hooks, caching fetched docs, or protecting annotated code blocks from simplification."
---

# hooks

Lifecycle hook scripts originally designed for Claude Code, adapted for opencode's agent and skill system.

## Available Hooks

### sdd-cache (WebFetch Cache)
Cross-session HTTP cache with ETag/Last-Modified revalidation. Caches WebFetch results and transparently serves them on repeat requests when the origin confirms `304 Not Modified`.

**Files:** `scripts/sdd-cache-pre.sh`, `scripts/sdd-cache-post.sh`
**Agent:** `sdd-cache` (auto-invoked by recommend skill)

### simplify-ignore (Code Block Protection)
Protects annotated code blocks during simplification by replacing them with hash placeholders. Prevents the model from modifying performance-critical or auto-generated code.

**Files:** `scripts/simplify-ignore.sh`, `scripts/simplify-ignore-test.sh`
**Agent:** `simplify-ignore`

## Usage

Invoke the hook scripts directly from any agent or skill:

```bash
# sdd-cache: pre-fetch
echo '{"tool_input":{"url":"...","prompt":"..."}}' | bash $HOOKS_DIR/sdd-cache-pre.sh

# sdd-cache: post-fetch  
echo '{"tool_input":{"url":"..."},"tool_response":"..."}' | bash $HOOKS_DIR/sdd-cache-post.sh

# simplify-ignore: pre-read or post-edit
echo '{}' | bash $HOOKS_DIR/simplify-ignore.sh
```
