---
name: hermes-domain-documentation
description: Skill for mapping, documenting, and cleaning up the Hermes agent's internal directory (~/.hermes/). Use when you need to understand what exists, identify redundancies, noise, duplicates, and plan cleanup before adding new components.
---

# Hermes Domain Documentation Skill

## Description
Skill for mapping, documenting, and cleaning up the Hermes agent's internal directory (`~/.hermes/`). Use when you need to understand what exists, identify redundancies, noise, duplicates, and plan cleanup before adding new components.

## Triggers
- User requests a map or inventory of the `.hermes` directory.
- User wants to document functionality of files and subdirectories.
- Prior to adding new major components (e.g., new vault, skill) to assess current state.
- Periodic maintenance audits.

## Steps
1. **Telemetry 360°** – Gather OS, hardware, runtime, environment variables, active services, disk usage.
2. **Profile Operational** – Define domain, objective, restrictions, success criteria.
3. **Generate Structural Map** – List all directories and files (excluding caches and hidden) with sizes.
4. **Document Functionality** – For each directory/file, describe purpose based on naming, content (README, SKILL.md, etc.), and observed usage.
5. **Classify Items** – Mark each as essential, useful, obsolete, duplicate, or candidate for archival/removal.
6. **Produce Cleanup Plan** – Recommend actions: keep, archive, delete, consolidate.
7. **Output Results** – Write a markdown file (e.g., in `memoria_superior/obsidian_vault/`) containing the map, documentation, classification, and recommendations.

## Outputs
- A structured map (`hermes_domain_map.md`) with directory sizes and tree.
- A detailed documentation file (`hermes_domain_documentation.md`) describing each item.
- A cleanup recommendations file (`hermes_domain_cleanup_plan.md`).

## Pitfalls
- Do not delete items without verifying they are not referenced by active configurations or skills.
- Avoid removing hidden state files (e.g., `.gateway_state_*.tmp`, lock files) unless certain they are stale.
- Be cautious with `node_modules`, `skills`, and `plugins` directories — they may contain critical functionality.
- Always back up before removal.

## References
- Internal Hermes directory layout conventions.
- Best practices for data retention and cleanup in agent systems.