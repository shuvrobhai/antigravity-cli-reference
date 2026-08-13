"""Tests for the config validation mode (issue #4)."""

from pathlib import Path

from check_consistency import validate_config

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "config"


def _exit_codes(folder: str) -> dict[str, int]:
    return {p.name: validate_config(p) for p in sorted((FIXTURES / folder).iterdir())}


def test_valid_fixtures_pass():
    codes = _exit_codes("valid")
    assert set(codes) == {"settings.json", "hooks.json", "mcp_config.json", "agent.md"}
    for name, code in codes.items():
        assert code == 0, f"{name} should validate cleanly, got exit {code}"


def test_invalid_fixtures_fail_naming_the_offending_fields(capsys):
    codes = _exit_codes("invalid")
    assert set(codes) == {"settings.json", "hooks.json", "mcp_config.json", "agent.md"}
    for name, code in codes.items():
        assert code == 1, f"{name} should fail validation, got exit {code}"

    out = capsys.readouterr().out
    assert "$.altScreenMode" in out
    assert "$.enableTelemetry" in out
    assert "$.toolPermission" in out
    assert "PreToolUse[0].matcher" in out
    assert "timeout" in out
    assert "$.mcpServers" in out
    assert "url" in out
    assert "httpUrl" in out
    assert "$.tools" in out
    assert "view_fille" in out
    assert "turbo" in out
    assert "sometimes" in out
