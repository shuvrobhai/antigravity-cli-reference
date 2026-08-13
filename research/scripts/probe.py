"""Deep module owning live agy CLI tool enumeration (issue #13).

Single seam for asking "which tools does the live CLI expose?". The real
adapter spawns `agy -p hello --output-format stream-json`, streams its
output line-by-line, and returns the tool set from the `init` event,
terminating the child as soon as the event is seen. A fake adapter (any
callable yielding stream-json lines) can be injected for tests, so the
parsing logic is exercised with no `agy` binary installed.
"""

import json
import os
import select
import subprocess
import time
from collections.abc import Callable, Iterable

AGY_CMD = ["agy", "-p", "hello", "--output-format", "stream-json"]
DEFAULT_TIMEOUT = 30.0


class ProbeError(Exception):
    """Raised when the live probe cannot produce a tool set."""


def live_tools(
    adapter: Callable[[], Iterable[str]] | None = None,
    *,
    timeout: float = DEFAULT_TIMEOUT,
) -> set[str]:
    """Enumerate the tools the live agy CLI exposes.

    Reads stream-json lines from ``adapter`` (default: a real ``agy``
    subprocess), returns the ``init`` event's tool set, and raises
    ``ProbeError`` when no ``init`` event is observed. The child process is
    terminated as soon as the event is found.
    """
    lines = _agy_lines(timeout) if adapter is None else adapter()
    try:
        return _tools_from_init(lines)
    finally:
        close = getattr(lines, "close", None)
        if close is not None:
            close()


def _tools_from_init(lines: Iterable[str]) -> set[str]:
    """Extract the tool set from the init event in a stream-json line stream."""
    for line in lines:
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or event.get("event") != "init":
            continue
        init = event.get("init")
        tools = init.get("tools") if isinstance(init, dict) else None
        if not isinstance(tools, list):
            raise ProbeError("init event did not carry a 'tools' list")
        return {str(tool) for tool in tools}
    raise ProbeError("no init event observed in agy stream-json output")


def _agy_lines(timeout: float) -> Iterable[str]:
    """Yield stream-json lines from a real agy subprocess; terminate on close."""
    try:
        proc = subprocess.Popen(
            AGY_CMD,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError as e:
        raise ProbeError(f"could not start agy: {e}") from e
    try:
        yield from _iter_lines(proc.stdout, timeout)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5.0)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()


def _iter_lines(stream, timeout: float) -> Iterable[str]:
    """Yield lines from a text stream, enforcing a wall-clock deadline."""
    deadline = time.monotonic() + timeout
    if os.name != "nt" and hasattr(select, "select"):
        yield from _iter_lines_posix(stream, deadline)
        return
    for line in stream:
        if time.monotonic() > deadline:
            raise ProbeError(
                f"agy probe timed out after {timeout:g}s without an init event"
            )
        yield line.rstrip("\r")


def _iter_lines_posix(stream, deadline: float) -> Iterable[str]:
    """Read lines via select-guarded chunked reads so a hung CLI cannot stall."""
    fd = stream.fileno()
    buf = ""
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ProbeError("agy probe timed out waiting for stream-json output")
        ready, _, _ = select.select([fd], [], [], remaining)
        if not ready:
            raise ProbeError("agy probe timed out waiting for stream-json output")
        chunk = os.read(fd, 65536).decode("utf-8", errors="replace")
        if not chunk:
            break
        buf += chunk
        while "\n" in buf:
            line, buf = buf.split("\n", 1)
            yield line.rstrip("\r")
    if buf:
        yield buf.rstrip("\r")
