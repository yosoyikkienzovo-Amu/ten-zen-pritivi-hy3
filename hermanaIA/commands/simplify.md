---
description: Simplify recent code
agent: build
---
Review and simplify the most recent code changes.

!git diff HEAD~3 --name-only

For each changed file:
1. Identify unnecessary complexity — over-engineering, redundant abstractions, dead code
2. Simplify without changing behavior — fewer lines, clearer logic, fewer dependencies
3. Preserve type safety, error handling, and test coverage

Output the simplified version and a diff summary.
