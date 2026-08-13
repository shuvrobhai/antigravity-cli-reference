"""Tests for the knowledge module (issue #15)."""

import json

import paths
import pytest
from knowledge import Knowledge, KnowledgeError

FIXTURE = {
    "version": "9.9.9",
    "last_verified": "2026-01-01",
    "commands": {
        "source": "DOCS",
        "confidence": "A",
        "entries": [
            {"command": "/alpha", "description": "Alpha"},
            {"command": "/beta", "description": "Beta"},
        ],
    },
    "tools": {
        "source": "DOCS",
        "confidence": "A",
        "entries": [
            {"name": "tool_a", "description": "A", "args_verified": True},
            {"name": "tool_b", "description": "B"},
        ],
    },
    "config_keys": {
        "entries": [
            {"key": "alpha", "source": "GOOGLE", "confidence": "B"},
            {"key": "beta"},
        ],
    },
    "transcript_schema": {
        "fields": [
            {"field": "type", "values": ["INIT", "STEP"]},
            {"field": "status", "values": ["SUCCESS"]},
            {"field": "note", "type": "string"},
        ],
    },
    "headless": {"status_enum": [{"status": "SUCCESS"}, {"status": "FAILED"}]},
    "extensibility": {
        "hooks": {"definition_fields": [{"field": "PreToolUse"}, {"field": "Stop"}]}
    },
    "known_gaps": {"entries": [{"question": "q1", "context": "c1"}]},
    "hard_gaps": {"entries": [{"gap": "g1", "status": "open"}]},
    "paths": {"entries": [{"path": "~/.x", "source": "DOCS", "confidence": "A"}]},
}


@pytest.fixture
def knowledge(tmp_path):
    p = tmp_path / "knowledge.json"
    p.write_text(json.dumps(FIXTURE), encoding="utf-8")
    return Knowledge(p)


def test_tools(knowledge):
    assert knowledge.tools() == {"tool_a", "tool_b"}


def test_config_keys(knowledge):
    assert knowledge.config_keys() == {"alpha", "beta"}


def test_transcript_enums_only_include_enum_fields(knowledge):
    assert knowledge.transcript_enums() == {
        "type": {"INIT", "STEP"},
        "status": {"SUCCESS"},
    }


def test_transcript_fields(knowledge):
    assert knowledge.transcript_fields() == {"type", "status", "note"}


def test_claims(knowledge):
    assert {c["command"] for c in knowledge.claims("commands")} == {"/alpha", "/beta"}
    assert knowledge.claims("known_gaps") == [{"question": "q1", "context": "c1"}]


def test_headless_statuses(knowledge):
    assert knowledge.headless_statuses() == {"SUCCESS", "FAILED"}


def test_version_and_last_verified(knowledge):
    assert knowledge.version() == "9.9.9"
    assert knowledge.last_verified() == "2026-01-01"


def test_sections(knowledge):
    assert {"version", "commands", "tools"} <= knowledge.sections()


def test_container_tags(knowledge):
    assert knowledge.container_tags("tools") == {"source": "DOCS", "confidence": "A"}
    assert knowledge.container_tags("config_keys") == {}


def test_hook_events(knowledge):
    assert knowledge.hook_events() == {"PreToolUse", "Stop"}


def test_unknown_claim_kind_raises_clean_error(knowledge):
    with pytest.raises(KnowledgeError, match="unknown claim kind"):
        knowledge.claims("nope")


def test_missing_file_raises_clean_error(tmp_path):
    with pytest.raises(KnowledgeError, match="not found"):
        Knowledge(tmp_path / "missing.json")


def test_bad_json_raises_clean_error(tmp_path):
    p = tmp_path / "knowledge.json"
    p.write_text("{ this is not json", encoding="utf-8")
    with pytest.raises(KnowledgeError, match="not valid JSON"):
        Knowledge(p)


def test_missing_container_raises_clean_error(tmp_path):
    p = tmp_path / "knowledge.json"
    p.write_text(json.dumps({"version": "1.0.0"}), encoding="utf-8")
    with pytest.raises(KnowledgeError, match="tools"):
        Knowledge(p).tools()


def test_default_path_is_the_canonical_knowledge_file():
    assert Knowledge().path == paths.knowledge_json()
