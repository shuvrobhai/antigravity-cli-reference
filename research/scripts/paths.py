"""Canonical repository file locations.

Single source of truth for where the research artifacts live. Every script in
this directory resolves locations through this module instead of computing
paths by hand, so a repository reorganization is a single edit here.

The anchor is this module's own location (research/scripts/paths.py). The
research root and the repository root are derived from it, and every accessor
is expressed relative to those roots.
"""

from pathlib import Path

_RESEARCH = Path(__file__).resolve().parent.parent
_REPO = _RESEARCH.parent

# Raw working copy of the research document, kept outside the repo (../raw/).
RAW_DOC_FILENAME = " Google Antigravity CLI: Complete Developer Reference and Documentation Gap Analysis.md"


def research_dir() -> Path:
    """The research/ directory: docs, schema, scripts, and audits live here."""
    return _RESEARCH


def repo_root() -> Path:
    """The repository root (the parent of research/)."""
    return _REPO


def scripts_dir() -> Path:
    """The research/scripts/ directory: the verification and sync suite."""
    return _RESEARCH / "scripts"


def knowledge_json() -> Path:
    """The machine-readable knowledge file (schema/antigravity-cli-knowledge.json)."""
    return _RESEARCH / "schema" / "antigravity-cli-knowledge.json"


def reference_doc() -> Path:
    """The canonical prose reference document (docs/antigravity-cli-reference.md)."""
    return _RESEARCH / "docs" / "antigravity-cli-reference.md"


def audits_dir() -> Path:
    """The evidence artifacts directory (research/audits)."""
    return _RESEARCH / "audits"


def schemas_dir() -> Path:
    """The JSON Schema validator files directory (research/schemas)."""
    return _RESEARCH / "schemas"


def raw_doc() -> Path:
    """The raw working-copy document kept outside the repo (../raw/)."""
    return _REPO.parent / "raw" / RAW_DOC_FILENAME
