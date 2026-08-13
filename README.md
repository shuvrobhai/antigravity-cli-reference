# Antigravity CLI Reference

A hand-maintained, source-classified reference for **Google Antigravity CLI** (`agy`) — every schema, path, configuration key, command, tool, and behavioral contract, built for humans and agents.

> Google Antigravity is a recent release that falls after most AI knowledge cutoffs. This repository exists so agents (and developers) can answer questions about it **from verified data instead of guesses**.

## What This Is

This repository answers three questions:

1. **What exists?** — Every configuration key, file path, command, tool argument, and schema in Antigravity CLI.
2. **What do the official docs tell you?** — Everything confirmed at `antigravity.google/docs/*`, with source attribution.
3. **What don't the official docs tell you?** — Behavioral gaps, undocumented contracts, and things that still require live verification.

## Repository Layout

| Path | Contents |
|---|---|
| `research/docs/antigravity-cli-reference.md` | The full research document (v5.1) — every claim tagged with source + confidence |
| `research/schema/antigravity-cli-knowledge.json` | Machine-readable knowledge file for agents (v1.1.0, fully populated — 45 paths, 35 commands, 30 config keys, 56 tools, extensibility schemas, and all known gaps) |
| `research/scripts/` | Verification tooling: `check_consistency.py` (doc↔JSON guard), `sync_docs.py` (working-copy sync), `gen_schemas.py` (schema regeneration), `capture_tools.py` + `test_tools_consistency.py` (live tool inventory), `audit_transcripts.py` (transcript enum audit), `diff_settings.py` (undocumented settings discovery) |
| `research/audits/` | Read-only evidence artifacts (transcript enum audit) |
| `.agents/rules/` | Repository agent operational guardrails & command references |
| `README.md` | This file |

## Provenance System

Every claim in the research document carries two tags:

- **Source:** `[DOCS]` (official docs) · `[GOOGLE]` (other Google sources) · `[PROTOCOL]` (MCP specification) · `[COMMUNITY]` (third-party)
- **Confidence:** `A` (confirmed by sources) · `B` (reasonable inference) · `C` (requires independent verification)

Never treat a `[COMMUNITY]` or `C` claim as fact.

## Status

- **2026-08-11 (v5.1):** All hard gaps re-verified against live docs. Resolved: headless `status` enum + exit codes, `general.defaultApprovalMode` enum, CLI brain directory path, and the `transcript.jsonl` line schema (verified hands-on with `agy` 1.1.11). Confirmed live: the plugins/subagents `agents/` documentation inconsistency (load behavior still untested).
- **JSON knowledge file v1.1.0:** Fully populated from the research document. Every entry carries `source` and `confidence` tags; sections marked with `_description` or empty entries are intentional (either guidance or not-yet-documented behavior).
- **Transcript enum audit (2026-08-11):** `research/scripts/audit_transcripts.py` scanned 49,586 lines across all 33 local brain sessions — `type` enum expanded to 19 values (9 promoted with citations), `status` confirmed as `DONE`/`RUNNING`/`ERROR`. Evidence in `research/audits/`.
- **Pure Research Reference:** `research/schema/` + `research/docs/` are canonical. This repository is dedicated exclusively to verified Antigravity CLI research, schemas, documentation, and consistency tooling.

## Development

```bash
uv run python research/scripts/check_consistency.py   # doc ↔ JSON + freshness guard (14 checks)
uv run ruff check research/scripts/                   # lint
uv run ruff format --check research/scripts/          # format gate
uv run python research/scripts/test_tools_consistency.py  # live CLI tool inventory (needs agy + auth)
uv run python research/scripts/diff_settings.py            # undocumented settings.json keys (needs local config)
```

## Related

- [`google-antigravity-docs/`](../google-antigravity-docs/) — offline mirror of the official docs, auto-synced from `antigravity.google/llms.txt`. This repo is the hand-maintained analysis layer on top of that mirror.

## License & Attribution

The research document summarizes public documentation and third-party sources; official documentation content is © Google. The original analysis and structure in this repository are provided for personal and reference use.

