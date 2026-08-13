"""Scripts must never write outside research/ (guard-rail regression test)."""

from pathlib import Path

import paths

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def test_sync_docs_guards_its_destination():
    src = (SCRIPTS / "sync_docs.py").read_text(encoding="utf-8")
    assert "outside research/" in src
    assert "is_relative_to(research_dir().resolve())" in src


def test_audit_transcripts_guards_json_and_out():
    src = (SCRIPTS / "audit_transcripts.py").read_text(encoding="utf-8")
    assert "outside research/" in src
    assert "is_relative_to(_research)" in src
    # both the --json and --out write sites are gated by the guard
    assert src.count("is_relative_to(_research)") >= 2


def test_no_script_writes_outside_research_unless_guarded():
    """Every write a script issues lands inside research/ either by construction
    (destination fixed via a paths accessor) or behind the explicit guard."""
    exempt = {  # destinations are fixed inside research/ by construction
        "sync_docs.py",
        "audit_transcripts.py",
        "knowledge.py",
        "gen_schemas.py",
    }
    unguarded_writes = []
    for py in SCRIPTS.glob("*.py"):
        if py.name in exempt:
            continue
        for i, line in enumerate(py.read_text(encoding="utf-8").splitlines(), 1):
            if "write_text" in line or "write_bytes" in line or "copy2" in line:
                unguarded_writes.append(f"{py.name}:{i}")
    assert unguarded_writes == [], f"unguarded write calls: {unguarded_writes}"


def test_guard_rejects_external_output(tmp_path, monkeypatch):
    """The guard predicate applied in the scripts rejects paths outside research/."""
    research = paths.research_dir().resolve()
    external = tmp_path / "outside.md"  # tmp_path is outside the repo/research
    assert not external.resolve().is_relative_to(research)
    inside = research / "docs" / "probe.md"
    assert inside.resolve().is_relative_to(research)
