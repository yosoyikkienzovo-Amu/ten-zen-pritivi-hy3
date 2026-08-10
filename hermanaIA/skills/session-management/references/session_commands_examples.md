# Session Management Command Examples

These are real examples from a Hermes session where the user wanted to improve session organization.

## Renaming a Session to a Meaningful Title

Instead of remembering cryptic IDs like `20260713_221229_d6aa91`, we renamed it to "Diagnóstico":

```bash
hermes sessions rename 20260713_221229_d6aa91 Diagnóstico
```

## Finding Sessions Later

After renaming, we could easily find the session:

```bash
# Search by keyword in session content
session_search(query="Diagnóstico", limit=1)

# Or list all sessions and look for the title
hermes sessions list
```

## Cleaning Up Unnecessary Sessions

We removed two empty/simple sessions that were just "hola" greetings:

```bash
# First verify what we want to delete
echo y | hermes sessions delete 20260713_172216_f74d44
echo y | hermes sessions delete 20260713_171903_f8daba
```

## Setting a Title During a Session

For future sessions, we can set a meaningful title right at the start:

```
/title Diagnóstico del sistema
```

Or rename later if needed:

```bash
hermes sessions rename "Diagnóstico" "Diagnóstico del sistema actualizado"
```

## Checking Session Information

To see details about a specific session:

```bash
hermes sessions show Diagnóstico
```

This would show the session ID, creation time, last activity, and message count.