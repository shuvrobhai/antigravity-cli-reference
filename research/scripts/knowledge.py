"""Deep module owning the Knowledge file's location, parse, and shape.

Single seam for Knowledge file access across the tooling tier. The four
consumers (consistency checker, tool-consistency checker, settings diff, and
transcript auditor) read the file only through this module, so a container key
or nesting change is one edit here instead of five. The transcript audit's
``promote`` write-back mutates through this module as well, so the mutation
logic is not duplicated in the script.

Canonical file locations live in the separate ``paths`` module (issue #12);
this module imports the Knowledge path from there and owns only shape
navigation. On a missing or malformed container it raises ``KnowledgeError``
with a descriptive message instead of a raw ``KeyError``.
"""

import json
from pathlib import Path

from paths import knowledge_json


class KnowledgeError(Exception):
    """Raised when the Knowledge file is missing, unreadable, or malformed."""


# Kinds whose claims live in a {kind: {"entries": [...]}} container.
CLAIM_KINDS = ("commands", "paths", "config_keys", "tools", "known_gaps", "hard_gaps")


class Knowledge:
    """Owns the Knowledge file's path, parse, and shape navigation."""

    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path is not None else knowledge_json()
        if not self.path.is_file():
            raise KnowledgeError(f"knowledge file not found: {self.path}")
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise KnowledgeError(f"knowledge file is not valid JSON: {e}") from e
        if not isinstance(data, dict):
            raise KnowledgeError(
                f"knowledge file must contain a JSON object: {self.path}"
            )
        self._data = data

    def _container(self, kind: str) -> dict:
        container = self._data.get(kind)
        if not isinstance(container, dict):
            raise KnowledgeError(
                f"required section {kind!r} is missing or not an object in {self.path}"
            )
        return container

    def _entries(self, kind: str) -> list:
        entries = self._container(kind).get("entries")
        if not isinstance(entries, list):
            raise KnowledgeError(
                f"section {kind!r} is missing its 'entries' list in {self.path}"
            )
        return entries

    def sections(self) -> set[str]:
        """The set of top-level sections present in the file."""
        return set(self._data)

    def version(self) -> str:
        """The knowledge file version string."""
        return str(self._data.get("version", ""))

    def last_verified(self) -> str:
        """The last-verified date string."""
        return str(self._data.get("last_verified", ""))

    def tools(self) -> set[str]:
        """The documented tool names (tools.entries[].name)."""
        return {e["name"] for e in self._entries("tools") if "name" in e}

    def config_keys(self) -> set[str]:
        """The documented config keys (config_keys.entries[].key)."""
        return {e["key"] for e in self._entries("config_keys") if "key" in e}

    def transcript_enums(self) -> dict[str, set[str]]:
        """The documented {field: values} enums from transcript_schema.fields."""
        return {
            f["field"]: set(f.get("values", []))
            for f in self._transcript_fields()
            if f.get("values") and "field" in f
        }

    def transcript_fields(self) -> set[str]:
        """Every documented transcript field name."""
        return {f["field"] for f in self._transcript_fields() if "field" in f}

    def headless_statuses(self) -> set[str]:
        """The documented headless status enum values."""
        container = self._container("headless")
        enum = container.get("status_enum")
        if not isinstance(enum, list):
            raise KnowledgeError(
                f"section 'headless' is missing its 'status_enum' list in {self.path}"
            )
        return {e.get("status") for e in enum if e.get("status")}

    def claims(self, kind: str) -> list[dict]:
        """The claim entries for a kind (commands, paths, config_keys, tools, ...)."""
        if kind not in CLAIM_KINDS:
            raise KnowledgeError(
                f"unknown claim kind {kind!r}; expected one of {sorted(CLAIM_KINDS)}"
            )
        return self._entries(kind)

    def container_tags(self, kind: str) -> dict[str, str]:
        """Section-level source/confidence tags for a container, if present."""
        container = self._container(kind)
        return {
            tag: container[tag] for tag in ("source", "confidence") if tag in container
        }

    def hook_events(self) -> set[str]:
        """The documented hook definition fields (extensibility.hooks.definition_fields)."""
        container = self._container("extensibility")
        hooks = container.get("hooks")
        if not isinstance(hooks, dict):
            raise KnowledgeError(
                f"section 'extensibility' is missing its 'hooks' object in {self.path}"
            )
        fields = hooks.get("definition_fields")
        if not isinstance(fields, list):
            raise KnowledgeError(
                "section 'extensibility.hooks' is missing its 'definition_fields' list "
                f"in {self.path}"
            )
        return {f["field"] for f in fields if f.get("field")}

    def promote_transcript_enums(
        self, additions: dict[str, dict[str, str]], stamp: str
    ) -> None:
        """Append newly observed transcript enum values with citation notes, then save.

        ``additions`` maps field name to {value: first-observation citation}.
        Each affected field gets the values appended (no duplicates) and a
        citation note describing the promotion.
        """
        fields = self._transcript_fields()
        note = f" (promoted by audit {stamp}): " + "; ".join(
            f"{value} first observed {cite}"
            for field, cites in additions.items()
            for value, cite in sorted(cites.items())
        )
        for field, cites in additions.items():
            for f in fields:
                if f.get("field") == field and "values" in f:
                    for value in sorted(cites):
                        if value not in f["values"]:
                            f["values"].append(value)
                    f["note"] = (f.get("note", "") + note).strip()
                    break
        self._save()

    def _save(self) -> None:
        """Persist the in-memory data back to the Knowledge file (canonical format)."""
        self.path.write_text(json.dumps(self._data, indent=2) + "\n", encoding="utf-8")

    def _transcript_fields(self) -> list:
        container = self._container("transcript_schema")
        fields = container.get("fields")
        if not isinstance(fields, list):
            raise KnowledgeError(
                f"section 'transcript_schema' is missing its 'fields' list in {self.path}"
            )
        return fields
