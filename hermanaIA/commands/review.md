---
description: Review recent changes
agent: plan
---
Review recent code changes using multi-axis analysis.

!git log --oneline -10
!git diff --stat

Evaluate:
1. **Correctness** — does the logic handle all edge cases?
2. **Simplicity** — could it be simpler without losing quality?
3. **Security** — any exposed secrets, injection vectors, or unsafe patterns?
4. **Consistency** — matches codebase conventions and style?
5. **Completeness** — are tests, error handling, and types adequate?

Provide actionable feedback per file. Prioritize issues by severity.
