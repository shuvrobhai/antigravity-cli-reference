"""Tests for the transcript audit split (issue #14)."""

import json
from pathlib import Path

from audit_transcripts import audit, promote
from knowledge import Knowledge

DOCUMENTED = {
    "type": {"INIT", "STEP"},
    "source": {"USER", "MODEL"},
    "status": {"SUCCESS"},
}


def _write_transcript(brain_dir: Path, conv: str, name: str, lines: list[str]) -> None:
    logs = brain_dir / conv / ".system_generated" / "logs"
    logs.mkdir(parents=True)
    (logs / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _knowledge_file(tmp_path, fields) -> Path:
    data = {"version": "1.0.0", "transcript_schema": {"fields": fields}}
    p = tmp_path / "knowledge.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def test_audit_finds_undocumented_values_with_citations(tmp_path):
    _write_transcript(
        tmp_path / "brain",
        "conv-1",
        "transcript-1.jsonl",
        [
            '{"type": "INIT", "source": "USER", "status": "SUCCESS"}',
            '{"type": "RESPONSE", "source": "MODEL", "status": "SUCCESS"}',
            '{"type": "RESPONSE", "source": "MODEL", "status": "FAILED"}',
        ],
    )
    result = audit(tmp_path / "brain", DOCUMENTED)

    assert result.transcript_lines == 3
    assert result.findings == {
        "type": {"RESPONSE": "conv-1:transcript-1.jsonl:2"},
        "status": {"FAILED": "conv-1:transcript-1.jsonl:3"},
    }


def test_audit_returns_no_findings_when_everything_documented(tmp_path):
    _write_transcript(
        tmp_path / "brain",
        "conv-1",
        "transcript-1.jsonl",
        ['{"type": "INIT", "source": "USER", "status": "SUCCESS"}'],
    )
    result = audit(tmp_path / "brain", DOCUMENTED)

    assert result.transcript_lines == 1
    assert result.findings == {}


def test_audit_is_read_only(tmp_path):
    kf = _knowledge_file(tmp_path, [{"field": "type", "values": ["INIT", "STEP"]}])
    before = kf.read_text(encoding="utf-8")
    _write_transcript(
        tmp_path / "brain",
        "conv-1",
        "transcript-1.jsonl",
        ['{"type": "INIT", "source": "USER", "status": "SUCCESS"}'],
    )
    audit(tmp_path / "brain", DOCUMENTED)
    assert kf.read_text(encoding="utf-8") == before


def test_promote_appends_values_and_citation_notes(tmp_path):
    kf = _knowledge_file(
        tmp_path,
        [
            {"field": "type", "values": ["INIT"]},
            {"field": "status", "values": ["SUCCESS"]},
        ],
    )
    findings = {
        "type": {"RESPONSE": "conv-1:transcript-1.jsonl:2"},
        "status": {"FAILED": "conv-1:transcript-1.jsonl:3"},
    }

    assert promote(kf, findings, "2026-08-12T00:00:00Z") == 0

    data = json.loads(kf.read_text(encoding="utf-8"))
    fields = {f["field"]: f for f in data["transcript_schema"]["fields"]}
    assert fields["type"]["values"] == ["INIT", "RESPONSE"]
    assert fields["status"]["values"] == ["SUCCESS", "FAILED"]
    assert "promoted by audit 2026-08-12T00:00:00Z" in fields["type"]["note"]
    assert (
        "RESPONSE first observed conv-1:transcript-1.jsonl:2" in fields["type"]["note"]
    )
    assert (
        "FAILED first observed conv-1:transcript-1.jsonl:3" in fields["status"]["note"]
    )


def test_promote_does_not_duplicate_existing_values(tmp_path):
    kf = _knowledge_file(tmp_path, [{"field": "type", "values": ["INIT", "RESPONSE"]}])
    promote(kf, {"type": {"RESPONSE": "conv-1:transcript-1.jsonl:2"}}, "stamp")

    data = json.loads(kf.read_text(encoding="utf-8"))
    assert data["transcript_schema"]["fields"][0]["values"] == ["INIT", "RESPONSE"]


def test_promote_writes_through_the_knowledge_module(tmp_path):
    kf = _knowledge_file(tmp_path, [{"field": "type", "values": ["INIT"]}])

    Knowledge(kf).promote_transcript_enums(
        {"type": {"RESPONSE": "conv-1:transcript-1.jsonl:2"}}, "stamp"
    )

    data = json.loads(kf.read_text(encoding="utf-8"))
    assert data["transcript_schema"]["fields"][0]["values"] == ["INIT", "RESPONSE"]
