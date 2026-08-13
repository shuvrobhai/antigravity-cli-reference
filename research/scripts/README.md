# Research & Verification Scripts

Tooling for the Antigravity CLI reference: consistency checks, schema regeneration, and live-CLI verification. Runs on Python 3.14+ via `uv`. Scripts only ever write inside `research/`.

## Run Every Script the Same Way

```bash
uv run python research/scripts/<script>.py [args]
```

The three modules below are libraries. Do not run them directly; other scripts import them.

| Script | Purpose |
|---|---|
| `paths.py` | Canonical file locations. One edit here re-routes every script after a reorg. |
| `knowledge.py` | Parses and navigates the knowledge file (deep module). |
| `probe.py` | Enumerates the live `agy` CLI's tools by reading its stream-json output. |

## Verification

| Script | What it checks | Needs |
|---|---|---|
| `check_consistency.py` | Research doc ↔ knowledge JSON stay in sync; the four JSON Schemas match the knowledge file; `--validate FILE` validates a settings/hooks/mcp_config/agent file against its inferred schema | `jsonschema` + `pyyaml` for `--validate`; no `agy` needed |
| `test_tools_consistency.py` | Documented tool set equals the live CLI's tool set | Running `agy` (with auth) |
| `diff_settings.py` | Real `settings.json` keys missing from the knowledge file; `--check` exits 1 on undocumented keys (CI gate) | Local `settings.json` |
| `audit_transcripts.py` | Observed transcript enums (`type`, `source`, `status`) vs documented; emits evidence to `research/audits/`. `--promote` writes new values back into the knowledge JSON with citations | Local brain transcripts |

## Schema Management

| Script | Purpose |
|---|---|
| `gen_schemas.py` | Regenerates the four `research/schemas/*.schema.json` validators from the knowledge file; `--check` exits 1 on drift |
| `check_consistency.py --validate <file>` | Validates one config file against its inferred schema |

## Sync & Capture

| Script | Purpose |
|---|---|
| `sync_docs.py` | Copies the working copy (`../raw/`) into `research/docs/`, then runs the consistency check |
| `capture_tools.py` | Dumps the live CLI tool list as sorted JSON |
| ~~`sync_skill.py`~~ | **Removed** — the skill is linked (not copied) via symlinks under `.agents/skills/`; scripts write only inside `research/` |

## CI

`.github/workflows/consistency.yml` runs on push to `main`: ruff lint + format check, `check_consistency.py`, and `pytest research/tests/`.