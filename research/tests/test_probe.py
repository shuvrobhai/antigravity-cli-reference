"""Tests for the probe module (issue #13)."""

import pytest
from probe import ProbeError, live_tools

INIT = '{"event": "init", "init": {"tools": ["tool_a", "tool_b", "tool_a"]}}'
MESSAGE = '{"event": "message", "message": "hello"}'
NOT_JSON = "this is not json"


def fake(*lines):
    """A fake adapter: a callable yielding the given stream-json lines."""
    return lambda: lines


def test_live_tools_returns_init_tool_set():
    assert live_tools(fake(MESSAGE, INIT)) == {"tool_a", "tool_b"}


def test_live_tools_skips_blank_and_unparseable_lines():
    assert live_tools(fake("", "   ", NOT_JSON, INIT)) == {"tool_a", "tool_b"}


def test_live_tools_deduplicates_repeated_tools():
    assert live_tools(fake(INIT)) == {"tool_a", "tool_b"}


def test_live_tools_raises_when_init_never_observed():
    with pytest.raises(ProbeError, match="no init event"):
        live_tools(fake(MESSAGE, NOT_JSON, ""))


def test_live_tools_raises_on_empty_stream():
    with pytest.raises(ProbeError, match="no init event"):
        live_tools(fake())


def test_live_tools_raises_when_init_lacks_tools_list():
    with pytest.raises(ProbeError, match="tools"):
        live_tools(fake('{"event": "init", "init": {}}'))
