# AGENTS.md

Operational reference and behavioral guardrails for agents working in the `antigravity-cli-reference` repo. Follow the "Would an agent likely miss this?" test — only repo-specific, hard-earned context is here.

---

## What this repo is

A hand-maintained, source-classified reference for **Google Antigravity CLI (`agy`)** — every config key, path, command, tool, and schema. It exists so agents answer questions about an AI product that postdates most training cutoffs **from verified, source-tagged data instead of guessing**.

Two canonical artifacts drive everything (editing either triggers `check_consistency.py`):

- `research/docs/antigravity-cli-reference.md` — prose reference; every claim tagged `[DOCS]`/`[GOOGLE]`/`[PROTOCOL]`/`[COMMUNITY]` (source) and `A`/`B`/`C` (confidence).
- `research/schema/antigravity-cli-knowledge.json` — machine-readable, source-tagged knowledge graph agents actually query.

> Never present `[COMMUNITY]` or confidence-`C` claims as fact. If data isn't in the knowledge base, answer *"Not documented in the knowledge base – unverified."*

---

## Runtime queries vs. maintenance scripts — don't confuse them

This is the single most important distinction in the repo. `research/scripts/` is **maintenance/CI tooling**, not a runtime query engine.

- **Answering questions** about Antigravity CLI → targeted `jq` queries against `antigravity-cli-knowledge.json`, or `sed` slices of the markdown doc. Do **not** run the Python scripts.
- **Do not whole-file `cat`** the knowledge JSON (96 KB) or markdown (80 KB) — always `jq` / line-slice.
- **Scripts run only** after changing the canonical files they guard (see below). Otherwise they're slow and irrelevant.

---

## Core commands (all via `uv`, Python 3.14+)

```bash
# Desync guard — run after editing doc OR knowledge JSON
uv run python research/scripts/check_consistency.py
# Validate a user config (settings.json / hooks.json / mcp_config.json / agent .md)
uv run python research/scripts/check_consistency.py --validate <file>
# Regenerate research/schemas/*.schema.json from the knowledge file (--check = dry run, exit 1 on drift)
uv run python research/scripts/gen_schemas.py
# Lint + format gate (CI) + tests
uv run ruff check research/scripts/
uv run ruff format --check research/scripts/
uv run pytest research/tests/
```

Notes:
- Tests live in **`research/tests/`** (CI runs `pytest research/tests/`). The root `tests/` directory holds only fixtures — don't look there for tests.
- CI (`.github/workflows/consistency.yml`, on push/PR to `main`) runs: ruff lint + format check, `check_consistency.py`, `pytest research/tests/`. Nothing else gates commits.
- **Maintenance scripts never write outside `research/`.**

---

## Maintenance scripts — when they run

| Script | Purpose | Needs |
|---|---|---|
| `check_consistency.py` | doc ↔ JSON sync, 4 schemas match knowledge file, `--validate FILE` | `jsonschema`+`pyyaml` for `--validate`; no `agy` |
| `gen_schemas.py` | regenerate `research/schemas/*.schema.json` from knowledge JSON | — |
| `sync_docs.py` | copy ext-repo `../raw/` working copy into `research/docs/` | raw doc outside repo |
| `test_tools_consistency.py` | documented tools == live `agy` tool set | running `agy` + auth |
| `diff_settings.py` | real `settings.json` keys missing from knowledge file (`--check` = CI gate, exit 1) | local `settings.json` |
| `audit_transcripts.py` | transcript enums vs documented; emits evidence to `research/audits/`; `--promote` writes back | local brain transcripts |
| `capture_tools.py` | dump live `agy` tool list as sorted JSON | running `agy` |

`paths.py`, `knowledge.py`, `probe.py` are **libraries**, not runnable scripts — other scripts import them. `paths.py` (`research/scripts/paths.py`) is the single source of truth for canonical file locations: after any file reorg, edit it once and every script re-routes.

---

## Directory map (what actually matters to an agent)

- `research/` — canonical: `docs/`, `schema/`, `schemas/` (generated validators), `scripts/`, `audits/` (read-only evidence), `tests/`. **Everything the maintenance scripts write stays inside `research/`.**
- `.agents/rules/` — `commands.md` (full command list), `conventions.md` (provenance + guardrails). Read these for detail; this file is the summary.
- `CONTEXT.md` — controlled-domain terminology dictionary.

---

## Conventions & guardrails worth preserving

- **Provenance tags are mandatory** whenever you state a fact about `agy` — cite source + confidence.
- **Zero-hallucination**: ground every claim in the knowledge files; else "unverified."
- **Permission gate**: ask before mutating shell commands (`agy`, `git`, `sed`), editing workspace files, or installing plugins.
- **`BLE001` / broad exception handling** is intentional in CLI scripts (see `pyproject.toml`); don't "fix" it.
- Offline doc mirror lives in a sibling repo `google-antigravity-docs/` — this repo is the hand-maintained analysis layer on top.

