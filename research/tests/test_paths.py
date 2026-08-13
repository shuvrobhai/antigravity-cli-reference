"""Tests for the canonical paths module (issue #12)."""

import paths

RESEARCH = paths.research_dir()
REPO = paths.repo_root()


def test_accessors_resolve_inside_the_repo():
    for accessor in (
        paths.knowledge_json,
        paths.reference_doc,
        paths.audits_dir,
    ):
        assert str(accessor()).startswith(str(REPO)), (
            f"{accessor.__name__}() escaped the repo: {accessor()}"
        )


def test_expected_absolute_locations():
    assert (
        paths.knowledge_json() == RESEARCH / "schema" / "antigravity-cli-knowledge.json"
    )
    assert paths.reference_doc() == RESEARCH / "docs" / "antigravity-cli-reference.md"
    assert paths.audits_dir() == RESEARCH / "audits"
    assert paths.scripts_dir() == RESEARCH / "scripts"
    assert paths.raw_doc() == REPO.parent / "raw" / paths.RAW_DOC_FILENAME


def test_documented_locations_exist_on_disk():
    for accessor in (
        paths.knowledge_json,
        paths.reference_doc,
        paths.audits_dir,
        paths.scripts_dir,
    ):
        assert accessor().exists(), (
            f"{accessor.__name__}() does not exist: {accessor()}"
        )


def test_raw_doc_is_absolute():
    # The raw working copy lives outside the repo (../raw/) and may be absent
    # in CI, so only its resolution — not its existence — is asserted.
    assert paths.raw_doc().is_absolute()
