# Command Reference

All Python scripts require Python 3.14+ and should be executed using `uv`.

## Consistency & Verification (Primary Test Suite)

- **Doc ↔ JSON Consistency Check:**
  ```bash
  uv run python research/scripts/check_consistency.py
  ```
  *Validates hash and structural consistency between `research/docs/antigravity-cli-reference.md` and `research/schema/antigravity-cli-knowledge.json`, and cross-checks the JSON Schema validators under `research/schemas/` against the knowledge file.*

- **Validate a user config against its JSON Schema:**
  ```bash
  uv run python research/scripts/check_consistency.py --validate <file>
  ```
  *Infers the schema from the file name — `settings.json`, `hooks.json`, `mcp_config.json`, or an agent `.md` (YAML frontmatter parsed first) — and reports every validation error with its JSON path (issue #4).*

- **Live Tool Inventory Consistency:**
  ```bash
  uv run python research/scripts/test_tools_consistency.py
  ```
  *Verifies live `agy` CLI tool schemas against the machine-readable JSON knowledge file (requires active `agy` binary and auth).*

## Schema Regeneration

- **Regenerate the JSON Schema validators from the knowledge file:**
  ```bash
  uv run python research/scripts/gen_schemas.py
  ```
  *Rebuilds `research/schemas/*.schema.json` as a mechanical projection of the knowledge JSON; run after the knowledge file changes. `--check` compares without writing (exit 1 on drift).*

## Path-Layout Test Suite

- **Canonical paths module test:**
  ```bash
  uv run pytest research/tests/
  ```
  *Asserts every accessor in `research/scripts/paths.py` resolves to the expected absolute location and that documented locations exist on disk, so repository-layout drift is caught early.*

## Code Quality & Formatting

- **Linting:**
  ```bash
  uv run ruff check research/scripts/
  ```

- **Check Formatting:**
  ```bash
  uv run ruff format --check research/scripts/
  ```

- **Apply Formatting:**
  ```bash
  uv run ruff format research/scripts/
  ```

## Synchronization, Auditing & Tools Capture

- **Sync Working Docs:**
  ```bash
  uv run python research/scripts/sync_docs.py
  ```
  *Synchronizes documentation artifacts across active research working copies.*

- **Audit Transcripts:**
  ```bash
  uv run python research/scripts/audit_transcripts.py
  ```
  *Scans local brain session transcripts to audit enum values and status schemas.*

- **Capture Live Tools:**
  ```bash
  uv run python research/scripts/capture_tools.py
  ```
  *Dumps live CLI tool schemas from `agy` for analysis and verification.*

- **Undocumented Settings Discovery:**
  ```bash
  uv run python research/scripts/diff_settings.py
  ```
