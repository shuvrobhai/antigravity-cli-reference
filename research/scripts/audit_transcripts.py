#!/usr/bin/env python3
"""Audit local brain transcripts against the documented transcript JSONL enums.

Scans every transcript under the CLI brain directory, histograms the `type`,
`source`, and `status` values, and diffs them against the enums documented in
the knowledge JSON (transcript_schema.fields). Newly observed values are
reported as hard findings and saved as evidence under audits/ so the enum can
be promoted with a citation.

The work is split into two clearly separated seams:

- ``audit(brain_dir, documented)`` — a pure, read-only analysis that returns
  findings; it never touches the Knowledge file.
- ``promote(json_path, findings, stamp)`` — an explicit write-back that mutates
  the Knowledge file through the deep Knowledge module (issue #14).

Usage:
    python3 research/scripts/audit_transcripts.py [--brain DIR] [--json PATH] [--out PATH] [--promote]

Defaults point at the local brain (~/.gemini/antigravity-cli/brain) and the repo
knowledge file. --promote updates the knowledge JSON enums with any newly
observed values, citing the source transcript path and line index of the first
observation. Read-only unless --promote is given.

Exit codes:
    0  every observed value is documented (or promoted with --promote)
    1  new values observed that are not in the documented enum
"""

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from knowledge import Knowledge
from paths import audits_dir, knowledge_json, research_dir

JSON_DEFAULT = knowledge_json()
BRAIN_DEFAULT = Path.home() / ".gemini" / "antigravity-cli" / "brain"
AUDIT_DIR = audits_dir()


@dataclass
class AuditResult:
    """Result of a pure transcript audit: histograms, provenance, and findings."""

    transcript_lines: int
    histograms: dict[str, Counter[str]]
    first_seen: dict[str, dict[str, str]]
    findings: dict[str, dict[str, str]]


def load_documented_enums(json_path: Path) -> dict[str, set[str]]:
    """Extract the documented {field: values} enums from transcript_schema."""
    return Knowledge(json_path).transcript_enums()


def iter_transcript_lines(brain_dir: Path):
    """Yield (conversation_id, file_name, line_index, record) across all transcripts."""
    for conv_dir in sorted(brain_dir.iterdir()):
        if not conv_dir.is_dir():
            continue
        logs = conv_dir / ".system_generated" / "logs"
        if not logs.is_dir():
            continue
        for tf in sorted(logs.glob("transcript*.jsonl")):
            with tf.open(encoding="utf-8") as fh:
                for i, line in enumerate(fh, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        print(f"WARN  unparseable line {tf}:{i}", file=sys.stderr)
                        continue
                    yield conv_dir.name, tf.name, i, rec


def audit(brain_dir: Path, documented: dict[str, set[str]]) -> AuditResult:
    """Scan transcripts under ``brain_dir`` and return the observed enum findings.

    Pure read: never touches the Knowledge file. Findings map field name to
    {value: first-observation citation} for every value not documented.
    """
    histograms: dict[str, Counter[str]] = {field: Counter() for field in documented}
    # also track any enum-typed field we have not documented yet
    histograms.setdefault("type", Counter())
    histograms.setdefault("source", Counter())
    histograms.setdefault("status", Counter())

    first_seen: dict[str, dict[str, str]] = {
        field: {} for field in histograms
    }  # field -> value -> "conversation:file:line"

    n_lines = 0
    for conv, tf, line_idx, rec in iter_transcript_lines(brain_dir):
        n_lines += 1
        if not isinstance(rec, dict):
            continue
        for field, hist in histograms.items():
            value = rec.get(field)
            if value is not None:
                hist[str(value)] += 1
                if str(value) not in first_seen[field]:
                    first_seen[field][str(value)] = f"{conv}:{tf}:{line_idx}"

    findings: dict[str, dict[str, str]] = {}
    for field, hist in histograms.items():
        documented_vals = documented.get(field, set())
        new_vals = sorted(v for v in hist if v not in documented_vals)
        if new_vals:
            findings[field] = {v: first_seen[field][v] for v in new_vals}

    return AuditResult(
        transcript_lines=n_lines,
        histograms=histograms,
        first_seen=first_seen,
        findings=findings,
    )


def promote(json_path: Path, findings: dict[str, dict[str, str]], stamp: str) -> int:
    """Promote newly observed enum values into the Knowledge file with citations.

    Navigates the schema only through the deep Knowledge module; the mutation is
    a deliberate, explicit write-back behind the ``--promote`` gate.
    """
    Knowledge(json_path).promote_transcript_enums(findings, stamp)
    n = sum(len(cites) for cites in findings.values())
    print(f"promoted {n} value(s) into {json_path}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--brain", default=str(BRAIN_DEFAULT))
    ap.add_argument("--json", default=str(JSON_DEFAULT))
    ap.add_argument("--out", default="")
    ap.add_argument(
        "--promote",
        action="store_true",
        help="promote new values into the knowledge JSON",
    )
    args = ap.parse_args()

    brain_dir = Path(args.brain)
    json_path = Path(args.json)
    if not brain_dir.is_dir():
        print(f"FAIL  brain directory not found: {brain_dir}")
        return 1

    # Scripts never write outside research/: the knowledge file and any --out
    # evidence path must both resolve inside research/.
    _research = research_dir().resolve()
    if not json_path.resolve().is_relative_to(_research):
        print(
            f"FAIL  --json {json_path} is outside research/; "
            "scripts only write inside research/"
        )
        return 1
    if args.out and not Path(args.out).resolve().is_relative_to(_research):
        print(
            f"FAIL  --out {args.out} is outside research/; "
            "scripts only write inside research/"
        )
        return 1

    documented = load_documented_enums(json_path)
    result = audit(brain_dir, documented)

    if result.transcript_lines == 0:
        print(f"WARN  no transcript lines found under {brain_dir}")
        return 0

    # --- report ----------------------------------------------------------------
    stamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    report = {
        "generated_at": stamp,
        "brain_dir": str(brain_dir),
        "transcript_lines": result.transcript_lines,
        "histograms": {f: dict(h) for f, h in result.histograms.items()},
        "documented_enums": {f: sorted(v) for f, v in documented.items()},
        "new_values": result.findings,
    }
    out_path = (
        Path(args.out)
        if args.out
        else AUDIT_DIR / f"transcript-audit-{stamp[:10]}.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    for field in sorted(result.histograms):
        hist = result.histograms[field]
        documented_vals = documented.get(field, set())
        n_doc = len(documented_vals)
        n_new = sum(1 for v in hist if v not in documented_vals)
        print(f"{field:8s} {len(hist):4d} distinct ({n_doc} documented, {n_new} new):")
        for value in sorted(hist):
            mark = "" if value in documented_vals else "  <-- NEW"
            cite = (
                f"  first: {result.first_seen[field][value]}"
                if value not in documented_vals
                else ""
            )
            print(f"         {value!r:40s} x{hist[value]:5d}{mark}{cite}")

    if result.findings:
        print(
            f"\nFAIL  {sum(len(v) for v in result.findings.values())} undocumented value(s) observed"
        )
        print(f"evidence written to {out_path}")
        if args.promote:
            return promote(json_path, result.findings, stamp)
        print("re-run with --promote to add them to the knowledge JSON with citations")
        return 1

    print(
        f"\nok    all observed values are documented ({result.transcript_lines} lines); evidence: {out_path}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
