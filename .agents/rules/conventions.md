# Coding Conventions & Behavioral Constraints

## Provenance System & Data Integrity

Every claim in this repository carries explicit source and confidence tags:

- **Source Tags:** `[DOCS]` (official docs) · `[GOOGLE]` (other Google sources) · `[PROTOCOL]` (MCP spec) · `[COMMUNITY]` (third-party)
- **Confidence Levels:** `A` (confirmed) · `B` (reasonable inference) · `C` (requires independent verification)

> **Rule:** Never present `[COMMUNITY]` or confidence `C` claims as established facts.

## Zero-Hallucination & Querying Guardrails

- **No Whole-File Dumping**: Never `cat` or read entire knowledge files. Use `jq` for JSON queries and `sed`/line-slicing for Markdown section extraction.
- **Strict Verification**: If data is missing from the canonical sources, answer: *"Not documented in the knowledge base – unverified."*

## Desync Guardrail

Any modification to `research/docs/antigravity-cli-reference.md` or `research/schema/antigravity-cli-knowledge.json` **MUST** be verified immediately using:
```bash
uv run python research/scripts/check_consistency.py
```

## Permission Gate & Session Logging

- **Permission Gate**: Ask for explicit user approval before executing mutating shell commands (`agy`, `git`, `sed`), modifying workspace files, or installing plugins.
- **Session Journal Logging**: Log side-effecting operations and knowledge gaps to `$SKILL_DIR/memory/session-journal.jsonl`.

## Code Style & Exception Handling

- **Target Runtime:** Python `>=3.14` via `uv`.
- **Formatting & Linting:** Enforced by Ruff (`uv run ruff check` / `uv run ruff format`).
- **Exception Reporting:** CLI scripts intentionally catch broad exceptions (`BLE001` ignored in Ruff linting) to output clear error reporting rather than unhandled tracebacks.
