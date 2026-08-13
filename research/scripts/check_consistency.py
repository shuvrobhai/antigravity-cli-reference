#!/usr/bin/env python3
"""Consistency checker: validate schema/antigravity-cli-knowledge.json against the
research document so the two can't silently desync.

Usage:
    python3 research/scripts/check_consistency.py [--doc PATH] [--json PATH]

Defaults point at the repo layout (docs/antigravity-cli-reference.md and
schema/antigravity-cli-knowledge.json). Pass --doc to check against another
copy, e.g. the working document in raw/:
    python3 research/scripts/check_consistency.py --doc "../raw/ Google Antigravity CLI: Complete Developer Reference and Documentation Gap Analysis.md"

Exit codes:
    0  consistent (warnings may be present)
    1  hard mismatch found
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml
from knowledge import Knowledge, KnowledgeError
from paths import knowledge_json, raw_doc, reference_doc, schemas_dir

DOC_DEFAULT = reference_doc()
JSON_DEFAULT = knowledge_json()
RAW_DEFAULT = raw_doc()

# JSON Schema validator files, one per config surface (issue #4).
SCHEMA_FILES = {
    "settings": "settings.schema.json",
    "hooks": "hooks.schema.json",
    "mcp": "mcp-config.schema.json",
    "agent": "agent-frontmatter.schema.json",
}

REQUIRED_SECTIONS = [
    "product",
    "version",
    "last_verified",
    "legend",
    "models",
    "paths",
    "config_keys",
    "keybindings",
    "statusline_payload",
    "permissions",
    "commands",
    "tools",
    "extensibility",
    "sandbox",
    "headless",
    "browser",
    "artifacts",
    "enterprise",
    "transcript_schema",
    "known_gaps",
    "hard_gaps",
]


def section(text: str, start: str, end: str | None = None) -> str:
    """Return the doc slice from `start` heading to the next heading."""
    i = text.find(start)
    if i == -1:
        return ""
    j = len(text) if end is None else text.find(end, i)
    return text[i:j] if j != -1 else text[i:]


def parse_frontmatter(path: Path) -> dict:
    """Parse the leading YAML frontmatter (--- ... ---) of a markdown agent file."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError("file does not start with a --- YAML frontmatter block")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("unterminated --- YAML frontmatter block")
    data = yaml.safe_load(text[3:end].strip())
    if not isinstance(data, dict):
        raise TypeError("frontmatter must be a YAML mapping")
    return data


def validate_config(path: Path) -> int:
    """Validate a user config file against its inferred JSON Schema (--validate).

    The schema is inferred from the file name: settings.json, hooks.json,
    mcp_config.json, or any .md agent file (YAML frontmatter parsed first).
    Exit codes: 0 valid, 1 invalid (or not inferable).
    """
    name = path.name
    if name == "settings.json":
        schema_name = SCHEMA_FILES["settings"]
    elif name == "hooks.json":
        schema_name = SCHEMA_FILES["hooks"]
    elif name == "mcp_config.json":
        schema_name = SCHEMA_FILES["mcp"]
    elif path.suffix == ".md":
        schema_name = SCHEMA_FILES["agent"]
    else:
        print(
            f"FAIL  cannot infer a schema for {path}; expected settings.json, "
            "hooks.json, mcp_config.json, or an agent .md file"
        )
        return 1

    if schema_name == SCHEMA_FILES["agent"]:
        try:
            data = parse_frontmatter(path)
        except (OSError, TypeError, ValueError, yaml.YAMLError) as e:
            print(f"FAIL  {path}: {e}")
            return 1
    else:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except OSError as e:
            print(f"FAIL  {path}: {e}")
            return 1
        except json.JSONDecodeError as e:
            print(f"FAIL  {path} is not valid JSON: {e}")
            return 1

    try:
        schema = json.loads((schemas_dir() / schema_name).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"FAIL  cannot load schema {schema_name}: {e}")
        return 1

    errors = sorted(
        jsonschema.Draft7Validator(schema).iter_errors(data),
        key=lambda e: e.json_path,
    )
    if not errors:
        print(f"ok    {path} is valid against {schema_name}")
        return 0
    print(f"FAIL  {path} has {len(errors)} validation error(s) against {schema_name}:")
    for error in errors:
        print(f"      {error.json_path}: {error.message}")
    return 1


def _settings_enum_mismatches(knowledge: Knowledge, schema: dict) -> list[str]:
    """Compare every enum-bearing config key's schema enum against the knowledge file."""
    mismatches = []
    for entry in knowledge.claims("config_keys"):
        key = entry.get("key")
        enum = entry.get("enum")
        if not key or not enum:
            continue
        node = schema.get("properties", {})
        for i, part in enumerate(key.split(".")):
            if i > 0:
                node = node.get("properties", {})
            node = node.get(part)
            if node is None:
                mismatches.append(f"{key}: missing from settings schema")
                break
        else:
            schema_enum = node.get("enum")
            if schema_enum is None:
                mismatches.append(f"{key}: schema has no enum")
            elif set(schema_enum) != set(enum):
                mismatches.append(
                    f"{key}: schema enum {sorted(schema_enum)} "
                    f"!= knowledge enum {sorted(enum)}"
                )
    return mismatches


def _agent_tools_mismatch(knowledge: Knowledge, schema: dict) -> list[str]:
    """Compare the agent frontmatter tools enum against the documented tool set."""
    documented = knowledge.tools()
    schema_enum = (
        schema.get("properties", {}).get("tools", {}).get("items", {}).get("enum")
    )
    if schema_enum is None:
        return ["agent schema has no tools enum"]
    schema_set = set(schema_enum)
    if schema_set == documented:
        return []
    return [
        f"only in schema: {sorted(schema_set - documented)}",
        f"only in knowledge: {sorted(documented - schema_set)}",
    ]


def _hooks_fields_mismatch(knowledge: Knowledge, schema: dict) -> list[str]:
    """Compare the hooks schema group fields against the documented definition fields."""
    documented = knowledge.hook_events()
    group = schema.get("definitions", {}).get("hookGroup", {}).get("properties", {})
    if not group:
        return ["hooks schema has no hookGroup definition"]
    schema_fields = set(group)
    if schema_fields == documented:
        return []
    return [
        f"only in schema: {sorted(schema_fields - documented)}",
        f"only in knowledge: {sorted(documented - schema_fields)}",
    ]


def _mcp_legacy_mismatch(schema: dict) -> list[str]:
    """Check the mcp schema rejects legacy url/httpUrl and requires one transport."""
    server = schema.get("definitions", {}).get("server", {})
    properties = server.get("properties", {})
    issues = []
    for legacy in ("url", "httpUrl"):
        if properties.get(legacy) is not False:
            issues.append(f"mcp schema does not reject legacy {legacy!r} field")
    one_of = server.get("oneOf")
    requireds = (
        {tuple(sorted(o.get("required", []))) for o in one_of} if one_of else set()
    )
    if ("command",) not in requireds or ("serverUrl",) not in requireds:
        issues.append("mcp schema does not require exactly one of command | serverUrl")
    return issues


def _main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--doc", default=str(DOC_DEFAULT))
    ap.add_argument("--json", default=str(JSON_DEFAULT))
    ap.add_argument("--freshness", default=str(RAW_DEFAULT))
    ap.add_argument(
        "--validate",
        metavar="FILE",
        help="validate a user config file against its inferred JSON Schema",
    )
    args = ap.parse_args()

    if args.validate:
        return validate_config(Path(args.validate))

    knowledge = Knowledge(args.json)

    doc = Path(args.doc).read_text(encoding="utf-8")
    doc_norm = doc.replace("`", "")  # backticks-free copy for membership checks

    results: list[tuple[str, bool, bool, str]] = []  # (label, hard, passed, detail)

    def check(label: str, hard: bool, passed: bool, detail: str = "") -> None:
        results.append((label, hard, passed, detail))

    # --- freshness check --------------------------------------------------
    if args.freshness:
        raw_path = Path(args.freshness)
        if raw_path.exists():
            doc_path = Path(args.doc)
            if doc_path.exists():
                raw_text = raw_path.read_text(encoding="utf-8")
                doc_text = doc_path.read_text(encoding="utf-8")

                raw_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
                doc_hash = hashlib.sha256(doc_text.encode("utf-8")).hexdigest()

                passed = raw_hash == doc_hash
                detail = ""
                if not passed:
                    raw_mtime = raw_path.stat().st_mtime
                    doc_mtime = doc_path.stat().st_mtime
                    if raw_mtime > doc_mtime:
                        detail = (
                            f"working copy (raw/) is newer ({raw_mtime} > {doc_mtime})"
                        )
                    else:
                        detail = f"published copy (docs/) is newer ({doc_mtime} > {raw_mtime})"
                    detail = f"divergence found: {detail}. hash raw={raw_hash[:8]} doc={doc_hash[:8]}"

                check(
                    "published copy matches working copy (freshness)",
                    True,
                    passed,
                    detail,
                )

    # --- structural -------------------------------------------------------
    missing = [s for s in REQUIRED_SECTIONS if s not in knowledge.sections()]
    check(
        "required top-level sections present",
        True,
        not missing,
        f"missing: {missing}" if missing else "",
    )
    check(
        "version is semver",
        True,
        bool(re.fullmatch(r"\d+\.\d+\.\d+", knowledge.version())),
    )
    check(
        "last_verified date appears in doc",
        False,
        knowledge.last_verified() in doc,
    )

    # --- commands ---------------------------------------------------------
    json_commands = {e["command"] for e in knowledge.claims("commands")}
    doc_cmd_rows = set(
        re.findall(
            r"^\| `/([a-z0-9-]+)(?: <[^>]+>)?`",
            section(doc, "## 7. Complete CLI", "## 8."),
            re.MULTILINE,
        )
    )
    doc_commands = {f"/{c}" for c in doc_cmd_rows}
    only_json = sorted(json_commands - doc_commands)
    only_doc = sorted(doc_commands - json_commands)
    check(
        "command set matches doc §7",
        True,
        json_commands == doc_commands,
        f"only in JSON: {only_json}; only in doc: {only_doc}"
        if only_json or only_doc
        else "",
    )
    check(
        "doc claims 35 commands and JSON agrees",
        True,
        len(json_commands) == 35 and len(doc_commands) == 35,
        f"json={len(json_commands)} doc={len(doc_commands)}",
    )

    # --- paths ------------------------------------------------------------
    missing_paths = []
    for entry in knowledge.claims("paths"):
        p = entry.get("path", "")
        if p and p not in doc_norm:
            missing_paths.append(p)
    check(
        "every JSON path appears in doc",
        True,
        not missing_paths,
        f"missing from doc: {missing_paths}" if missing_paths else "",
    )

    # --- config keys ------------------------------------------------------
    missing_keys = [
        k
        for k in (e.get("key") for e in knowledge.claims("config_keys"))
        if k and k not in doc_norm
    ]
    check(
        "every config key appears in doc",
        True,
        not missing_keys,
        f"missing from doc: {missing_keys}" if missing_keys else "",
    )

    # --- tools ------------------------------------------------------------
    missing_tools = [
        t
        for t in (e.get("name") for e in knowledge.claims("tools"))
        if t and t not in doc_norm
    ]
    check(
        "every tool name appears in doc",
        True,
        not missing_tools,
        f"missing from doc: {missing_tools}" if missing_tools else "",
    )

    # --- headless status enum ---------------------------------------------
    missing_status = [s for s in knowledge.headless_statuses() if s not in doc_norm]
    check(
        "every headless status value appears in doc",
        True,
        not missing_status,
        f"missing from doc: {missing_status}" if missing_status else "",
    )

    # --- transcript schema --------------------------------------------------
    missing_tf = [f for f in knowledge.transcript_fields() if f not in doc_norm]
    check(
        "every transcript schema field appears in doc",
        True,
        not missing_tf,
        f"missing from doc: {missing_tf}" if missing_tf else "",
    )

    # --- known gaps ---------------------------------------------------------
    json_gaps = {g["question"] for g in knowledge.claims("known_gaps")}
    doc_gap_section = section(doc, "## 17. Undocumented", "## 18.")
    doc_gap_rows = {
        m
        for m in re.findall(
            r"^\| (.*?) \| .*? \| .*? \|$", doc_gap_section, re.MULTILINE
        )
        if m and not m.startswith(("-", "Question"))
    }
    missing_gaps = [g for g in json_gaps if g not in doc_norm]
    check(
        "every known-gap question appears in doc",
        True,
        not missing_gaps,
        f"missing from doc: {missing_gaps}" if missing_gaps else "",
    )
    check(
        "known-gap counts roughly match",
        False,
        abs(len(json_gaps) - len(doc_gap_rows)) <= 3,
        f"json={len(json_gaps)} doc_rows={len(doc_gap_rows)}",
    )

    # --- hard gaps -----------------------------------------------------------
    missing_hg = [
        h["gap"] for h in knowledge.claims("hard_gaps") if h["gap"] not in doc_norm
    ]
    check(
        "every hard-gap name appears in doc",
        True,
        not missing_hg,
        f"missing from doc: {missing_hg}" if missing_hg else "",
    )

    # --- tag hygiene ---------------------------------------------------------
    untagged = []
    for kind in ("paths", "config_keys"):
        entries = knowledge.claims(kind)
        for e in entries:
            if "source" not in e or "confidence" not in e:
                untagged.append(
                    f"{kind}.{e.get('path' if kind == 'paths' else 'key', '?')}"
                )
    for kind in ("commands", "tools"):
        tags = knowledge.container_tags(kind)
        if "source" not in tags or "confidence" not in tags:
            untagged.append(f"{kind} (section-level tag missing)")
    for e in knowledge.claims("tools"):
        for flag in ("args_verified", "description_verified"):
            if flag not in e:
                untagged.append(f"tools.{e.get('name', '?')} missing {flag}")
    check(
        "claim entries carry source+confidence tags",
        False,
        not untagged,
        f"untagged: {untagged}" if untagged else "",
    )

    # --- schema <-> knowledge cross-checks -------------------------------------
    schemas: dict[str, dict] = {}
    for label, name in SCHEMA_FILES.items():
        path = schemas_dir() / name
        try:
            schemas[label] = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            check(f"schema {name} loads", True, False, str(e))

    if "settings" in schemas:
        settings_issues = _settings_enum_mismatches(knowledge, schemas["settings"])
        check(
            "settings schema enums match knowledge config_keys",
            True,
            not settings_issues,
            "; ".join(settings_issues) if settings_issues else "",
        )
    if "agent" in schemas:
        agent_issues = _agent_tools_mismatch(knowledge, schemas["agent"])
        check(
            "agent frontmatter tools enum matches documented tool set",
            True,
            not agent_issues,
            "; ".join(agent_issues) if agent_issues else "",
        )
    if "hooks" in schemas:
        hooks_issues = _hooks_fields_mismatch(knowledge, schemas["hooks"])
        check(
            "hooks schema fields match documented hook definition fields",
            True,
            not hooks_issues,
            "; ".join(hooks_issues) if hooks_issues else "",
        )
    if "mcp" in schemas:
        mcp_issues = _mcp_legacy_mismatch(schemas["mcp"])
        check(
            "mcp schema rejects legacy url/httpUrl and requires one transport",
            True,
            not mcp_issues,
            "; ".join(mcp_issues) if mcp_issues else "",
        )

    # --- report ----------------------------------------------------------------
    n_fail = sum(1 for _, hard, passed, _ in results if hard and not passed)
    n_warn = sum(1 for _, hard, passed, _ in results if not hard and not passed)
    for label, hard, passed, detail in results:
        mark = "ok  " if passed else ("FAIL" if hard else "WARN")
        err_detail = f" ({detail})" if detail and not passed else ""
        print(f"{mark}  {label}{err_detail}")
    print(f"\n{len(results)} checks, {n_fail} hard failures, {n_warn} warnings")
    return 1 if n_fail else 0


def main() -> int:
    """Run the consistency checks, reporting structural failures cleanly."""
    try:
        return _main()
    except KnowledgeError as e:
        print(f"FAIL  {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
